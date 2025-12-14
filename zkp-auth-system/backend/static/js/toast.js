/**
 * Modern Toast Notification System
 * Replaces alert() with beautiful toast notifications
 */

class Toast {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        // Create toast container
        this.container = document.createElement('div');
        this.container.id = 'toast-container';
        this.container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            gap: 12px;
            pointer-events: none;
        `;
        document.body.appendChild(this.container);
    }

    show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };

        toast.innerHTML = `
            <div class="toast-content">
                <span class="toast-icon">${icons[type] || icons.info}</span>
                <span class="toast-message">${message}</span>
                <button class="toast-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        toast.style.cssText = `
            background: ${this.getBackgroundColor(type)};
            color: ${this.getTextColor(type)};
            padding: 16px 20px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(20px);
            border: 1px solid ${this.getBorderColor(type)};
            min-width: 300px;
            max-width: 400px;
            animation: toastSlideIn 0.3s ease;
            pointer-events: auto;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
        `;

        // Add styles if not already added
        if (!document.getElementById('toast-styles')) {
            const style = document.createElement('style');
            style.id = 'toast-styles';
            style.textContent = `
                @keyframes toastSlideIn {
                    from {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                @keyframes toastSlideOut {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                }
                .toast-content {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }
                .toast-icon {
                    font-size: 20px;
                    flex-shrink: 0;
                }
                .toast-message {
                    flex: 1;
                    line-height: 1.5;
                }
                .toast-close {
                    background: none;
                    border: none;
                    color: inherit;
                    font-size: 24px;
                    cursor: pointer;
                    padding: 0;
                    width: 24px;
                    height: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    opacity: 0.7;
                    transition: opacity 0.2s;
                    flex-shrink: 0;
                }
                .toast-close:hover {
                    opacity: 1;
                }
            `;
            document.head.appendChild(style);
        }

        this.container.appendChild(toast);

        // Auto remove
        if (duration > 0) {
            setTimeout(() => {
                toast.style.animation = 'toastSlideOut 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }, duration);
        }

        return toast;
    }

    getBackgroundColor(type) {
        const colors = {
            success: 'rgba(40, 167, 69, 0.2)',
            error: 'rgba(220, 53, 69, 0.2)',
            warning: 'rgba(255, 193, 7, 0.2)',
            info: 'rgba(102, 126, 234, 0.2)'
        };
        return colors[type] || colors.info;
    }

    getTextColor(type) {
        const colors = {
            success: '#28a745',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#ffffff'
        };
        return colors[type] || colors.info;
    }

    getBorderColor(type) {
        const colors = {
            success: 'rgba(40, 167, 69, 0.3)',
            error: 'rgba(220, 53, 69, 0.3)',
            warning: 'rgba(255, 193, 7, 0.3)',
            info: 'rgba(102, 126, 234, 0.3)'
        };
        return colors[type] || colors.info;
    }

    success(message, duration = 3000) {
        return this.show(message, 'success', duration);
    }

    error(message, duration = 4000) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration = 3000) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration = 3000) {
        return this.show(message, 'info', duration);
    }
}

// Global instance
const toast = new Toast();

// Replace alert function
window.showToast = toast;

