<script lang="ts">
    let prompt: string = '';
    let imageUrl: string = '';
    let inferenceSteps: number = 50;
    let guidanceScale: number = 3.0;
    let loading: boolean = false;
    let error: string | null = null;
    let negativePrompt: string = '';
    let width: number = 704;
    let height: number =  448;
    let videoBlob: Blob | null = null;
    let videoUrl: string | null = null;

    async function handleSubmit() {
        loading = true;
        error = null;
        if (videoUrl) {
            URL.revokeObjectURL(videoUrl);
            videoUrl = null;
            videoBlob = null;
        }
        
        try {
            const backendUrl = import.meta.env.VITE_BACKEND_URL;
            if (!backendUrl) {
                throw new Error('Backend URL is not configured. Please check your environment variables.');
            }

            // Create the request payload with parameter names
            const payload = {
                prompt: prompt,
                negative_prompt: negativePrompt || null,
                image_url: imageUrl,
                num_inference_steps: inferenceSteps || null,
                width: width || null,
                height: height || null,
                guidance_scale: guidanceScale || null
            };

            const response = await fetch(`${backendUrl}/generate-video`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                console.log(response);
                throw new Error(`Failed to generate video: ${response.statusText}`);
            }

            // Handle binary video data directly
            const videoData = await response.blob();
            videoBlob = new Blob([videoData], { type: 'video/mp4' });
            videoUrl = URL.createObjectURL(videoBlob);

        } catch (e) {
            error = e instanceof Error ? e.message : 'An unknown error occurred';
            console.error('Error details:', e);
        } finally {
            loading = false;
        }
    }
</script>

<div class="container">
    <h1>Video Generator</h1>
    
    <div class="layout-container">
        <div class="form-section">
            <form on:submit|preventDefault={handleSubmit}>
                <div class="form-group">
                    <label for="imageUrl">Image URL (only PNG images):</label>
                    <input 
                        id="imageUrl"
                        type="url" 
                        bind:value={imageUrl} 
                        required
                    />
                </div>

                <div class="form-group">
                    <label for="prompt">Prompt:</label>
                    <textarea 
                        id="prompt"
                        bind:value={prompt} 
                        required
                        rows="3"
                        placeholder="Write here what you want to happen in the video..."
                    ></textarea>
                </div>

                <div class="form-group">
                    <label for="negativePrompt">Negative Prompt:</label>
                    <textarea 
                        id="negativePrompt"
                        bind:value={negativePrompt} 
                        rows="3"
                        placeholder="This field is optional. Write here what you don't want in the video..."
                    ></textarea>
                </div>

                <div class="form-row">
                    <div class="form-group half">
                        <label for="width">Width:</label>
                        <input 
                            id="width"
                            type="number" 
                            bind:value={width} 
                            min="64"
                            step="64"
                        />
                    </div>

                    <div class="form-group half">
                        <label for="height">Height:</label>
                        <input 
                            id="height"
                            type="number" 
                            bind:value={height} 
                            min="64"
                            step="64"
                        />
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group half">
                        <label for="inferenceSteps">Number of Inference Steps:</label>
                        <input 
                            id="inferenceSteps"
                            type="number" 
                            bind:value={inferenceSteps} 
                            min="1" 
                            max="100"
                        />
                    </div>

                    <div class="form-group half">
                        <label for="guidanceScale">Guidance Scale:</label>
                        <input 
                            id="guidanceScale"
                            type="number" 
                            bind:value={guidanceScale} 
                            step="0.1" 
                            min="1" 
                            max="20"
                        />
                    </div>
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? 'Generating...' : 'Generate Video'}
                </button>
            </form>

            {#if error}
                <div class="error">
                    {error}
                </div>
            {/if}
        </div>

        <div class="video-section">
            {#if videoUrl}
                <div class="video-container">
                    <h2>Generated Video:</h2>
                    <!-- svelte-ignore a11y-media-has-caption -->
                    <video controls>
                        <source src={videoUrl} type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <a href={videoUrl} download="generated-video.mp4" class="download-button">
                        Download Video
                    </a>
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
    .container {
        max-width: 1200px;
        margin: 2rem auto;
        padding: 3rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    }

    h1 {
        color: #2c3e50;
        margin-bottom: 2rem;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 600;
    }

    .layout-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 3rem;
        align-items: start;
    }

    .form-section {
        width: 100%;
    }

    .video-section {
        width: 100%;
        min-height: 200px; /* Ensures the right column exists even when empty */
    }

    .video-container {
        position: sticky;
        top: 2rem;
        width: 100%;
    }

    .form-group {
        margin-bottom: 2rem;
    }

    label {
        display: block;
        margin-bottom: 0.5rem;
        color: #2c3e50;
        font-weight: 500;
    }

    input[type="url"],
    input[type="number"] {
        width: 100%;
        padding: 0.75rem;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        transition: all 0.2s;
        font-size: 1rem;
    }

    input:focus {
        outline: none;
        border-color: #4b5563;
        box-shadow: 0 0 0 3px rgba(75, 85, 99, 0.1);
    }

    button {
        background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 500;
        width: 100%;
        transition: all 0.2s;
    }

    button:hover:not(:disabled) {
        background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(31, 41, 55, 0.2);
    }

    button:disabled {
        background: #e2e8f0;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }

    .error {
        color: #dc2626;
        margin-top: 1rem;
        padding: 1rem;
        background-color: #fee2e2;
        border-radius: 8px;
        border: 1px solid #fecaca;
    }

    video {
        width: 100%;
        max-width: 100%;
        border-radius: 8px;
        margin: 1rem 0;
    }

    .download-button {
        display: inline-block;
        background: #4b5563;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        text-decoration: none;
        margin-top: 1rem;
        transition: background-color 0.2s;
    }

    .download-button:hover {
        background: #374151;
    }

    @media (max-width: 1024px) {
        .layout-container {
            grid-template-columns: 1fr;
        }

        .video-container {
            position: static;
        }

        .video-section {
            min-height: auto;
        }
    }

    textarea {
        width: 100%;
        padding: 0.75rem;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        transition: all 0.2s;
        font-size: 1rem;
        resize: vertical;
        min-height: 80px;
        font-family: inherit;
    }

    textarea:focus {
        outline: none;
        border-color: #4b5563;
        box-shadow: 0 0 0 3px rgba(75, 85, 99, 0.1);
    }

    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .form-group.half {
        margin-bottom: 0;
    }

    .form-group.half input[type="number"] {
        width: 100px;  /* Set fixed width for numeric inputs in half groups */
    }

    /* Add this to ensure the labels don't force the containers to be too wide */
    .form-group.half label {
        white-space: nowrap;
        display: block;
        margin-bottom: 0.5rem;
    }

    /* Ensure the form-row containers align properly */
    .form-row .form-group.half {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    @media (max-width: 640px) {
        .form-row {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .form-group.half {
            margin-bottom: 1rem;
        }

        .form-group.half input[type="number"] {
            width: 100%; /* Full width on mobile */
        }
    }
</style>