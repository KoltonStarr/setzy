// Stub data for sales calls
const stubSalesCalls = [
    {
        id: 1,
        title: "Acme Corp - Q4 Review",
        date: "Dec 18, 2025",
        description: "Quarterly business review with key stakeholders discussing expansion opportunities.",
        duration: "45:32",
        sentiment: "Positive",
        status: "completed"
    },
    {
        id: 2,
        title: "TechStart Inc - Discovery Call",
        date: "Dec 17, 2025",
        description: "Initial discovery meeting to understand their sales automation needs.",
        duration: "32:15",
        sentiment: "Neutral",
        status: "completed"
    },
    {
        id: 3,
        title: "GlobalCo - Demo Session",
        date: "Dec 16, 2025",
        description: "Product demonstration for their sales leadership team.",
        duration: "28:45",
        sentiment: "Positive",
        status: "in-progress"
    },
    {
        id: 4,
        title: "StartupXYZ - Follow-up",
        date: "Dec 15, 2025",
        description: "Follow-up call to address concerns from previous meeting.",
        duration: "18:20",
        sentiment: "Positive",
        status: "completed"
    },
    {
        id: 5,
        title: "Enterprise Solutions - Contract Review",
        date: "Dec 14, 2025",
        description: "Final contract negotiations and timeline discussion.",
        duration: "52:10",
        sentiment: "Neutral",
        status: "completed"
    },
    {
        id: 6,
        title: "MidMarket Co - Initial Outreach",
        date: "Dec 13, 2025",
        description: "First touchpoint to introduce our platform capabilities.",
        duration: "15:30",
        sentiment: "Positive",
        status: "completed"
    }
];

// Stub chatbot responses
const stubChatbotResponses = [
    "That's a great question! Based on the sales calls I've analyzed, I can provide insights on call performance and sentiment.",
    "I've reviewed your recent calls. The average sentiment across all calls is positive, with strong engagement from prospects.",
    "Your most successful calls tend to be around 30-45 minutes long, with clear agenda and follow-up actions.",
    "I noticed that demo sessions have a 75% conversion rate when followed up within 24 hours.",
    "Let me analyze that for you. On average, your discovery calls last 28 minutes and focus on pain points.",
    "Great observation! The calls with TechStart and GlobalCo show similar patterns in objection handling.",
];

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeSalesCalls();
    initializeUpload();
    initializeChatbot();
});

// Sales Calls Functions
function initializeSalesCalls() {
    const salesCallsGrid = document.getElementById('salesCallsGrid');
    
    stubSalesCalls.forEach(call => {
        const card = createSalesCallCard(call);
        salesCallsGrid.appendChild(card);
    });
}

function createSalesCallCard(call) {
    const card = document.createElement('div');
    card.className = 'sales-call-card';
    card.onclick = () => handleCallClick(call);
    
    card.innerHTML = `
        <div class="card-header">
            <div class="card-title">${call.title}</div>
            <div class="card-status status-${call.status}">${call.status}</div>
        </div>
        <div class="card-date">${call.date}</div>
        <div class="card-description">${call.description}</div>
        <div class="card-stats">
            <div class="card-stat">
                <span class="stat-label">Duration</span>
                <span class="stat-value">${call.duration}</span>
            </div>
            <div class="card-stat">
                <span class="stat-label">Sentiment</span>
                <span class="stat-value">${call.sentiment}</span>
            </div>
        </div>
    `;
    
    return card;
}

function handleCallClick(call) {
    console.log('Clicked on call:', call);
    // Stub: Would open call details or playback
    alert(`Opening details for: ${call.title}\n\n(This is a stub - API integration needed)`);
}

// Upload Functions
function initializeUpload() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadStatus = document.getElementById('uploadStatus');
    const uploadMessage = document.getElementById('uploadMessage');
    
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    // Highlight drop zone when dragging over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('drag-over');
        });
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('drag-over');
        });
    });
    
    // Handle dropped files
    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        handleFiles(files);
    });
    
    // Handle file input change
    fileInput.addEventListener('change', (e) => {
        const files = e.target.files;
        handleFiles(files);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function handleFiles(files) {
        if (files.length === 0) return;
        
        const file = files[0];
        
        // Stub: Would normally upload to server
        console.log('File selected:', file.name, file.type, file.size);
        
        uploadStatus.classList.remove('hidden');
        uploadMessage.textContent = `Uploading: ${file.name} (${formatFileSize(file.size)})...`;
        
        // Simulate upload progress
        setTimeout(() => {
            uploadMessage.textContent = `✓ Successfully uploaded: ${file.name}`;
            
            // Add new stub call to the grid
            const newCall = {
                id: stubSalesCalls.length + 1,
                title: file.name.replace(/\.[^/.]+$/, ""),
                date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
                description: "Processing video and generating transcript...",
                duration: "--:--",
                sentiment: "Pending",
                status: "in-progress"
            };
            
            const salesCallsGrid = document.getElementById('salesCallsGrid');
            const card = createSalesCallCard(newCall);
            salesCallsGrid.insertBefore(card, salesCallsGrid.firstChild);
            
            // Reset file input
            fileInput.value = '';
            
            // Hide status after 3 seconds
            setTimeout(() => {
                uploadStatus.classList.add('hidden');
            }, 3000);
        }, 2000);
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }
}

// Chatbot Functions
function initializeChatbot() {
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    
    sendButton.addEventListener('click', sendMessage);
    
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    function sendMessage() {
        const message = chatInput.value.trim();
        
        if (message === '') return;
        
        // Add user message
        addMessage(message, 'user');
        
        // Clear input
        chatInput.value = '';
        
        // Disable input while "thinking"
        chatInput.disabled = true;
        sendButton.disabled = true;
        
        // Simulate bot response delay
        setTimeout(() => {
            const response = getStubResponse();
            addMessage(response, 'bot');
            
            // Re-enable input
            chatInput.disabled = false;
            sendButton.disabled = false;
            chatInput.focus();
        }, 1000 + Math.random() * 1000); // Random delay between 1-2 seconds
    }
    
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function getStubResponse() {
        // Return random stub response
        return stubChatbotResponses[Math.floor(Math.random() * stubChatbotResponses.length)];
    }
}
