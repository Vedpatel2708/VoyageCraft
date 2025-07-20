class TravelPlannerApp {
    constructor() {
        this.interests = [];
        this.groupSize = 1;
        this.currentStep = 0;
        this.loadingSteps = [
            'step1', 'step2', 'step3', 'step4', 'step5', 'step6', 'step7', 'step8'
        ];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.logStatus();
    }

    logStatus() {
        console.log('🌍 AI Travel Planner loaded successfully!');
        console.log('✅ Event listeners attached');
        console.log('📱 App ready for user interaction');
    }

    setupEventListeners() {
        // Form submission
        const tripForm = document.getElementById('tripForm');
        if (tripForm) {
            tripForm.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }
        
        // Interests input
        const interestsInput = document.getElementById('interests');
        if (interestsInput) {
            interestsInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.addInterest(interestsInput.value.trim());
                    interestsInput.value = '';
                }
            });
        }

        // Group size controls
        const decreaseBtn = document.getElementById('decreaseGroup');
        const increaseBtn = document.getElementById('increaseGroup');
        
        if (decreaseBtn) decreaseBtn.addEventListener('click', () => this.adjustGroupSize(-1));
        if (increaseBtn) increaseBtn.addEventListener('click', () => this.adjustGroupSize(1));

        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => this.switchTab(tab.dataset.tab));
        });

        // New plan button
        const newPlanBtn = document.getElementById('newPlanBtn');
        if (newPlanBtn) {
            newPlanBtn.addEventListener('click', () => this.resetForm());
        }
    }

    addInterest(interest) {
        if (interest && !this.interests.includes(interest)) {
            this.interests.push(interest);
            this.updateInterestsDisplay();
            console.log(`Added interest: ${interest}`);
        }
    }

    removeInterest(interest) {
        this.interests = this.interests.filter(i => i !== interest);
        this.updateInterestsDisplay();
        console.log(`Removed interest: ${interest}`);
    }

    updateInterestsDisplay() {
        const container = document.getElementById('interestsContainer');
        if (container) {
            container.innerHTML = this.interests.map(interest => `
                <div class="interest-tag">
                    ${interest}
                    <span class="remove" onclick="app.removeInterest('${interest}')">×</span>
                </div>
            `).join('');
        }
    }

    adjustGroupSize(delta) {
        this.groupSize = Math.max(1, Math.min(20, this.groupSize + delta));
        const display = document.getElementById('groupSizeDisplay');
        if (display) {
            display.textContent = this.groupSize;
        }
        console.log(`Group size adjusted to: ${this.groupSize}`);
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        console.log('🚀 Starting trip planning process...');
        
        const formData = this.collectFormData();
        
        if (!this.validateFormData(formData)) {
            return;
        }

        this.showLoading();
        this.startLoadingAnimation();

        try {
            console.log('📡 Sending request to API...');
            const response = await fetch('/api/plan-trip', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.error) {
                throw new Error(result.error);
            }

            console.log('✅ Trip planning successful!');
            this.displayResults(result, formData);
        } catch (error) {
            console.error('❌ Planning failed:', error);
            this.showError(`Failed to plan trip: ${error.message}`);
            this.hideLoading();
        }
    }

    collectFormData() {
        return {
            destination: document.getElementById('destination')?.value || '',
            duration: document.getElementById('duration')?.value || '',
            budget: document.getElementById('budget')?.value || 'mid-range',
            travelStyle: document.getElementById('travelStyle')?.value || 'cultural',
            interests: this.interests,
            specialRequests: document.getElementById('specialRequests')?.value || '',
            groupSize: this.groupSize
        };
    }

    validateFormData(formData) {
        if (!formData.destination || !formData.duration) {
            this.showError('Please fill in all required fields (destination and duration)');
            return false;
        }
        return true;
    }

    showLoading() {
        this.hideElement('tripForm');
        this.hideElement('resultsSection');
        this.hideElement('errorMessage');
        this.showElement('loadingSection');
        this.currentStep = 0;
        console.log('⏳ Loading screen displayed');
    }

    hideLoading() {
        this.hideElement('loadingSection');
        this.showElement('tripForm');
    }

    startLoadingAnimation() {
        const animateStep = () => {
            if (this.currentStep < this.loadingSteps.length) {
                // Mark previous step as completed
                if (this.currentStep > 0) {
                    const prevStep = document.getElementById(this.loadingSteps[this.currentStep - 1]);
                    if (prevStep) prevStep.className = 'loading-step completed';
                }
                
                // Mark current step as active
                const currentStep = document.getElementById(this.loadingSteps[this.currentStep]);
                if (currentStep) currentStep.className = 'loading-step active';
                
                this.currentStep++;
                setTimeout(animateStep, 1500);
            } else {
                // Mark last step as completed
                const lastStep = document.getElementById(this.loadingSteps[this.loadingSteps.length - 1]);
                if (lastStep) lastStep.className = 'loading-step completed';
            }
        };
        
        setTimeout(animateStep, 500);
    }

    displayResults(result, formData) {
        this.hideLoading();
        console.log('📊 Displaying results...');

        // Show success message
        const successMsg = document.getElementById('successMessage');
        if (successMsg) {
            successMsg.innerHTML = `✅ Your ${formData.duration} trip to ${formData.destination} is ready!`;
        }

        // Populate tab content
        this.populateTabContent('itineraryCard', result.itinerary);
        this.populateTabContent('budgetCard', result.budget);
        this.populateTabContent('tipsCard', result.tips);
        this.populateTabContent('transportCard', result.transportation);
        this.populateTabContent('hotelsCard', result.accommodation);

        // Show results section
        this.showElement('resultsSection');
        this.hideElement('errorMessage');

        // Reset to first tab
        this.switchTab('itinerary');

        console.log('✅ Results displayed successfully');
    }

    populateTabContent(cardId, content) {
        const card = document.getElementById(cardId);
        if (card && content) {
            card.innerHTML = this.formatContent(content);
        }
    }

    formatContent(content) {
        // If content is already HTML, return as is
        if (content.includes('<') && content.includes('>')) {
            return content;
        }
        
        // Otherwise, format plain text with basic HTML structure
        return `<div>${content.replace(/\n/g, '<br>')}</div>`;
    }

    switchTab(tabName) {
        // Remove active class from all tabs and content
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        // Add active class to selected tab and content
        const selectedTab = document.querySelector(`[data-tab="${tabName}"]`);
        const selectedContent = document.getElementById(`${tabName}-content`);

        if (selectedTab) selectedTab.classList.add('active');
        if (selectedContent) selectedContent.classList.add('active');

        console.log(`Switched to tab: ${tabName}`);
    }

    showError(message) {
        const errorElement = document.getElementById('errorMessage');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
        console.error('❌ Error displayed:', message);
    }

    hideError() {
        const errorElement = document.getElementById('errorMessage');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }

    showElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            if (elementId === 'loadingSection') {
                element.style.display = 'flex';
            } else {
                element.style.display = 'block';
            }
        }
    }

    hideElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = 'none';
        }
    }

    resetForm() {
        console.log('🔄 Resetting form...');
        
        // Reset form fields
        const form = document.getElementById('tripForm');
        if (form) {
            form.reset();
        }

        // Reset app state
        this.interests = [];
        this.groupSize = 1;
        this.currentStep = 0;

        // Update displays
        this.updateInterestsDisplay();
        const groupSizeDisplay = document.getElementById('groupSizeDisplay');
        if (groupSizeDisplay) {
            groupSizeDisplay.textContent = this.groupSize;
        }

        // Reset loading steps
        this.loadingSteps.forEach(stepId => {
            const step = document.getElementById(stepId);
            if (step) {
                step.className = 'loading-step';
            }
        });

        // Hide results and show form
        this.hideElement('resultsSection');
        this.hideElement('errorMessage');
        this.showElement('tripForm');

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });

        console.log('✅ Form reset completed');
    }

    // Utility method to handle API errors
    handleApiError(error, response) {
        let errorMessage = 'An unexpected error occurred';
        
        if (response) {
            switch (response.status) {
                case 400:
                    errorMessage = 'Invalid request. Please check your input.';
                    break;
                case 401:
                    errorMessage = 'Authentication failed. Please check API configuration.';
                    break;
                case 429:
                    errorMessage = 'Too many requests. Please try again later.';
                    break;
                case 500:
                    errorMessage = 'Server error. Please try again later.';
                    break;
                default:
                    errorMessage = error.message || errorMessage;
            }
        } else {
            errorMessage = error.message || errorMessage;
        }

        return errorMessage;
    }

    // Method to validate API response
    validateApiResponse(result) {
        const requiredFields = ['itinerary', 'budget', 'tips', 'transportation', 'accommodation'];
        
        for (const field of requiredFields) {
            if (!result[field]) {
                console.warn(`⚠️ Missing field in API response: ${field}`);
            }
        }

        return result;
    }

    // Method to sanitize HTML content
    sanitizeHTML(content) {
        const div = document.createElement('div');
        div.textContent = content;
        return div.innerHTML;
    }

    // Method to get current form state for debugging
    getFormState() {
        return {
            interests: this.interests,
            groupSize: this.groupSize,
            currentStep: this.currentStep,
            formData: this.collectFormData()
        };
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TravelPlannerApp();
    console.log('🚀 Travel Planner App initialized');
});

// Global error handler for unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    if (window.app) {
        window.app.showError('An unexpected error occurred. Please try again.');
        window.app.hideLoading();
    }
});

// Global error handler for JavaScript errors
window.addEventListener('error', (event) => {
    console.error('JavaScript error:', event.error);
    if (window.app) {
        window.app.showError('A technical error occurred. Please refresh the page.');
    }
});