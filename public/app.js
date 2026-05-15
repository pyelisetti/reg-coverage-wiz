// DOM elements
const questionnaireInput = document.getElementById('questionnaire-file');
const inventoryInput = document.getElementById('inventory-file');
const analyzeBtn = document.getElementById('analyze-btn');
const rerunBtn = document.getElementById('rerun-btn');
const spinner = document.getElementById('spinner');
const errorContainer = document.getElementById('error');
const errorMessage = document.getElementById('error-message');
const questionnaireNameDisplay = document.getElementById('questionnaire-name');
const inventoryNameDisplay = document.getElementById('inventory-name');

const welcomeMessage = document.getElementById('welcome-message');
const dataPanes = document.getElementById('data-panes');
const inventoryContent = document.getElementById('inventory-content');
const inventoryCount = document.getElementById('inventory-count');
const pauseInventoryBtn = document.getElementById('pause-inventory');
const resultsSummary = document.getElementById('results-summary');
const summaryContent = document.getElementById('summary-content');
const summaryColumn = document.getElementById('summary-column');
const executiveSummary = document.getElementById('executive-summary');
const coverageCardsContainer = document.getElementById('coverage-cards-container');
const questionnairePreview = document.getElementById('questionnaire-preview');
const inventoryPreview = document.getElementById('inventory-preview');

// Auto-scroll state
let inventoryScrollInterval = null;
let inventoryPaused = false;

// File input change handlers
questionnaireInput.addEventListener('change', (e) => {
    const fileName = e.target.files[0]?.name || '';
    questionnaireNameDisplay.textContent = fileName;
    updateAnalyzeButton();
});

inventoryInput.addEventListener('change', (e) => {
    const fileName = e.target.files[0]?.name || '';
    inventoryNameDisplay.textContent = fileName;
    updateAnalyzeButton();
});

// Enable analyze button only when both files are selected
function updateAnalyzeButton() {
    const hasQuestionnaire = questionnaireInput.files.length > 0;
    const hasInventory = inventoryInput.files.length > 0;
    const bothFilesSelected = hasQuestionnaire && hasInventory;

    // Validate file extensions
    let validFiles = true;
    if (hasQuestionnaire) {
        const qFile = questionnaireInput.files[0].name.toLowerCase();
        if (!qFile.endsWith('.xlsx') && !qFile.endsWith('.xls')) {
            validFiles = false;
        }
    }
    if (hasInventory) {
        const iFile = inventoryInput.files[0].name.toLowerCase();
        if (!iFile.endsWith('.xlsx') && !iFile.endsWith('.xls')) {
            validFiles = false;
        }
    }

    analyzeBtn.disabled = !(bothFilesSelected && validFiles);
}

// Analyze button click handler
analyzeBtn.addEventListener('click', async () => {
    await runAnalysis();
});

// Rerun button click handler
rerunBtn.addEventListener('click', async () => {
    await runAnalysis();
});

async function runAnalysis() {
    const formData = new FormData();
    formData.append('questionnaire', questionnaireInput.files[0]);
    formData.append('inventory', inventoryInput.files[0]);

    // Hide errors and stop any scrolling
    hideError();
    stopAutoScroll();

    // Clear previous data
    inventoryContent.innerHTML = '';
    summaryContent.innerHTML = '';
    coverageCardsContainer.innerHTML = '';

    // Show spinner
    showSpinner();
    hideWelcome();

    try {
        // First, get and display the prompt
        const promptFormData = new FormData();
        promptFormData.append('questionnaire', questionnaireInput.files[0]);
        promptFormData.append('inventory', inventoryInput.files[0]);

        const promptResponse = await fetch('/api/get-prompt', {
            method: 'POST',
            body: promptFormData
        });

        if (promptResponse.ok) {
            const promptData = await promptResponse.json();
            if (promptData.prompt && promptData.prompt.user) {
                try {
                    // Extract JSON data from the prompt
                    const userPrompt = promptData.prompt.user;

                    // Extract questionnaire JSON
                    const qMatch = userPrompt.match(/QUESTIONNAIRE:\s*(\[[\s\S]*?\])\s*INVENTORY:/);
                    const questionnaireData = qMatch ? JSON.parse(qMatch[1]) : [];

                    // Extract inventory JSON
                    const iMatch = userPrompt.match(/INVENTORY:\s*(\[[\s\S]*?\])$/);
                    const inventoryData = iMatch ? JSON.parse(iMatch[1]) : [];

                    // Display inventory data in pane
                    displayInventoryData(inventoryData);

                    // Show data previews in spinner
                    showDataPreviews(questionnaireData, inventoryData);
                } catch (parseError) {
                    console.error('Error parsing prompt data:', parseError);
                }
            }
        }

        // Show data panes and start auto-scroll
        showDataPanes();
        startAutoScroll();

        // Now proceed with the actual analysis
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        hideSpinner();

        if (!response.ok) {
            showError(data.error || 'An unexpected error occurred');
            return;
        }

        if (data.regulations && Array.isArray(data.regulations)) {
            // Display coverage cards in right panel
            displayCoverageCards(data.regulations);

            // Display sidebar summary (keep for quick reference)
            displayResults(data.regulations);

            // Display executive summary if available
            if (data.summary) {
                displayExecutiveSummary(data.summary);
            }

            showSummaryColumn();
            showRerunButton();
        } else {
            showError('Invalid response format from server');
        }

    } catch (error) {
        hideSpinner();
        showError(`Network error: ${error.message}`);
    }
}

// Display inventory data in pane
function displayInventoryData(data) {
    inventoryContent.innerHTML = '';
    inventoryCount.textContent = `${data.length} items`;

    data.forEach((item, index) => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'data-item';
        itemDiv.style.animationDelay = `${index * 0.05}s`;

        itemDiv.innerHTML = `
            <div class="data-item-header">
                <div class="data-item-title">${item.testName || 'N/A'}</div>
                <div class="data-item-badge badge-test">${item.id || 'N/A'}</div>
            </div>
            ${item.objective ? `
            <div class="data-item-field">
                <span class="field-label">Objective:</span>
                <span class="field-value long">${item.objective}</span>
            </div>
            ` : ''}
            ${item.regulation ? `
            <div class="data-item-field">
                <span class="field-label">Regulation:</span>
                <span class="field-value">${item.regulation}</span>
            </div>
            ` : ''}
            ${item.businessUnit ? `
            <div class="data-item-field">
                <span class="field-label">Business Unit:</span>
                <span class="field-value">${item.businessUnit}</span>
            </div>
            ` : ''}
            ${item.product ? `
            <div class="data-item-field">
                <span class="field-label">Product:</span>
                <span class="field-value">${item.product}</span>
            </div>
            ` : ''}
            ${item.frequency ? `
            <div class="data-item-field">
                <span class="field-label">Frequency:</span>
                <span class="field-value">${item.frequency}</span>
            </div>
            ` : ''}
        `;

        inventoryContent.appendChild(itemDiv);
    });
}

// Auto-scroll functions
function startAutoScroll() {
    inventoryPaused = false;
    pauseInventoryBtn.textContent = '⏸ Pause';

    // Scroll speed: 30px per second
    inventoryScrollInterval = setInterval(() => {
        if (!inventoryPaused) {
            inventoryContent.scrollTop += 1;
        }
    }, 33);
}

function stopAutoScroll() {
    if (inventoryScrollInterval) {
        clearInterval(inventoryScrollInterval);
        inventoryScrollInterval = null;
    }
}

// Pause button handler
pauseInventoryBtn.addEventListener('click', () => {
    inventoryPaused = !inventoryPaused;
    pauseInventoryBtn.textContent = inventoryPaused ? '▶ Resume' : '⏸ Pause';
});

// Display results in sidebar
function displayResults(regulations) {
    summaryContent.innerHTML = '';

    // Sort by coverage percent ascending (gaps first)
    const sorted = [...regulations].sort((a, b) => a.coveragePercent - b.coveragePercent);

    sorted.forEach(reg => {
        const status = computeStatus(reg.coveragePercent);
        const statusClass = getStatusClass(status);

        const itemDiv = document.createElement('div');
        itemDiv.className = 'summary-item';

        itemDiv.innerHTML = `
            <div class="summary-regulation">${reg.regulation}</div>
            <div class="summary-status">
                <span class="summary-coverage">${reg.coveragePercent}%</span>
                <div class="status-bubble ${statusClass}"></div>
            </div>
        `;

        summaryContent.appendChild(itemDiv);
    });

    resultsSummary.style.display = 'block';
}

// Compute status from coverage percent
function computeStatus(coveragePercent) {
    if (coveragePercent < 35) {
        return 'Gap';
    } else if (coveragePercent >= 35 && coveragePercent <= 60) {
        return 'Moderate';
    } else {
        return 'Strong';
    }
}

// Get CSS class suffix for status
function getStatusClass(status) {
    return status.toLowerCase();
}

// UI helper functions
function showSpinner() {
    spinner.style.display = 'flex';
}

function hideSpinner() {
    spinner.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorContainer.style.display = 'block';
}

function hideError() {
    errorContainer.style.display = 'none';
}

function hideWelcome() {
    welcomeMessage.style.display = 'none';
}

function showDataPanes() {
    dataPanes.style.display = 'flex';
}

function showRerunButton() {
    rerunBtn.style.display = 'block';
    analyzeBtn.style.display = 'none';
}

// Show data previews in spinner overlay
function showDataPreviews(questionnaireData, inventoryData) {
    // Show first 3 items from questionnaire
    questionnairePreview.innerHTML = '';
    const qSample = questionnaireData.slice(0, 3);
    qSample.forEach(item => {
        const previewDiv = document.createElement('div');
        previewDiv.className = 'preview-item';
        previewDiv.innerHTML = `
            <div class="preview-label">Question Code</div>
            <div class="preview-value">${item.questionCode || 'N/A'}</div>
            <div class="preview-label">Regulation</div>
            <div class="preview-value">${item.regulationSource || 'N/A'}</div>
            <div class="preview-label">Question</div>
            <div class="preview-value">${item.questionText || 'N/A'}</div>
        `;
        questionnairePreview.appendChild(previewDiv);
    });

    if (questionnaireData.length > 3) {
        const moreDiv = document.createElement('div');
        moreDiv.style.textAlign = 'center';
        moreDiv.style.color = '#718096';
        moreDiv.style.marginTop = '0.5rem';
        moreDiv.textContent = `... and ${questionnaireData.length - 3} more items`;
        questionnairePreview.appendChild(moreDiv);
    }

    // Show first 3 items from inventory
    inventoryPreview.innerHTML = '';
    const iSample = inventoryData.slice(0, 3);
    iSample.forEach(item => {
        const previewDiv = document.createElement('div');
        previewDiv.className = 'preview-item';
        previewDiv.innerHTML = `
            <div class="preview-label">Test ID</div>
            <div class="preview-value">${item.id || 'N/A'}</div>
            <div class="preview-label">Test Name</div>
            <div class="preview-value">${item.testName || 'N/A'}</div>
            <div class="preview-label">Regulation</div>
            <div class="preview-value">${item.regulation || 'N/A'}</div>
        `;
        inventoryPreview.appendChild(previewDiv);
    });

    if (inventoryData.length > 3) {
        const moreDiv = document.createElement('div');
        moreDiv.style.textAlign = 'center';
        moreDiv.style.color = '#718096';
        moreDiv.style.marginTop = '0.5rem';
        moreDiv.textContent = `... and ${inventoryData.length - 3} more items`;
        inventoryPreview.appendChild(moreDiv);
    }
}

// Display coverage cards in right panel
function displayCoverageCards(regulations) {
    coverageCardsContainer.innerHTML = '';

    // Sort by coverage percent ascending (gaps first)
    const sorted = [...regulations].sort((a, b) => a.coveragePercent - b.coveragePercent);

    sorted.forEach(reg => {
        const status = computeStatus(reg.coveragePercent);
        const statusClass = getStatusClass(status);

        const card = document.createElement('div');
        card.className = 'coverage-card';

        card.innerHTML = `
            <div class="coverage-card-header">
                <div class="regulation-name">${reg.regulation}</div>
                <div class="coverage-badge">
                    <span class="coverage-percent ${statusClass}">${reg.coveragePercent}%</span>
                </div>
            </div>
            <div class="coverage-status ${statusClass}">
                <span class="status-dot ${statusClass}"></span>
                <span>${status}</span>
            </div>
            <div class="coverage-details">
                <div>
                    <span class="detail-label">Covered:</span>
                    <span class="detail-value">${reg.coveredQuestions} / ${reg.totalQuestions}</span>
                </div>
                <div>
                    <span class="detail-label">Gaps:</span>
                    <span class="detail-value">${reg.totalQuestions - reg.coveredQuestions}</span>
                </div>
            </div>
        `;

        coverageCardsContainer.appendChild(card);
    });
}

// Display executive summary
function displayExecutiveSummary(summaryText) {
    // Convert line breaks to paragraphs
    const paragraphs = summaryText.split('\n\n').filter(p => p.trim());

    executiveSummary.innerHTML = '';
    paragraphs.forEach(paragraph => {
        const p = document.createElement('p');
        p.textContent = paragraph.trim();
        executiveSummary.appendChild(p);
    });
}

function showSummaryColumn() {
    summaryColumn.style.display = 'flex';
}

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    stopAutoScroll();
});
