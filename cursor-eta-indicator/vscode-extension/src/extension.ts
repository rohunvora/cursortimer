import * as vscode from 'vscode';
import * as child_process from 'child_process';
import * as path from 'path';

interface ETAStatus {
    eta_seconds: number;
    current_step: number;
    total_steps: number;
    tokens_used: number;
    tokens_expected: number;
    elapsed_seconds: number;
    progress_percent: number;
    current_description: string;
}

export function activate(context: vscode.ExtensionContext) {
    const etaManager = new CursorETAManager(context);
    
    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('cursorETA.showDetails', () => {
            etaManager.showDetails();
        }),
        vscode.commands.registerCommand('cursorETA.toggle', () => {
            etaManager.toggle();
        })
    );
    
    // Start monitoring
    etaManager.startMonitoring();
}

export function deactivate() {}

class CursorETAManager {
    private statusBar: vscode.StatusBarItem;
    private enabled: boolean = true;
    private currentStatus: ETAStatus | null = null;
    private hideTimer: NodeJS.Timeout | null = null;
    private process: child_process.ChildProcess | null = null;
    
    constructor(private context: vscode.ExtensionContext) {
        // Create status bar item
        const config = vscode.workspace.getConfiguration('cursorETA');
        const alignment = config.get<string>('alignment') === 'right' 
            ? vscode.StatusBarAlignment.Right 
            : vscode.StatusBarAlignment.Left;
        const priority = config.get<number>('priority', 100);
        
        this.statusBar = vscode.window.createStatusBarItem(alignment, priority);
        this.statusBar.command = 'cursorETA.showDetails';
        this.enabled = config.get<boolean>('enabled', true);
        
        context.subscriptions.push(this.statusBar);
        
        // Listen for configuration changes
        context.subscriptions.push(
            vscode.workspace.onDidChangeConfiguration(e => {
                if (e.affectsConfiguration('cursorETA')) {
                    this.updateConfiguration();
                }
            })
        );
    }
    
    startMonitoring() {
        // Look for Python wrapper processes
        this.findAndMonitorWrapper();
        
        // Also listen for terminal creation
        this.context.subscriptions.push(
            vscode.window.onDidOpenTerminal(terminal => {
                // Check if this terminal might be running our wrapper
                this.checkTerminalForWrapper(terminal);
            })
        );
    }
    
    private findAndMonitorWrapper() {
        // Try to find the Python wrapper script
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) return;
        
        // Look for agent_with_eta.py in common locations
        const possiblePaths = [
            'agent_with_eta.py',
            'python/agent_with_eta.py',
            '../python/agent_with_eta.py',
            path.join(__dirname, '../../python/agent_with_eta.py')
        ];
        
        // For now, we'll rely on terminals running the wrapper
        // In production, this could spawn the wrapper directly
    }
    
    private checkTerminalForWrapper(terminal: vscode.Terminal) {
        // In a real implementation, we'd check if the terminal
        // is running our Python wrapper and attach to its output
        // For MVP, we'll simulate by listening to workspace output
        this.simulateWrapperOutput();
    }
    
    private simulateWrapperOutput() {
        // Simulate receiving status updates
        // In production, this would parse actual stdout from the Python wrapper
        
        let step = 0;
        const interval = setInterval(() => {
            step++;
            if (step > 10) {
                clearInterval(interval);
                this.handleStatusLine('STATUS|COMPLETE');
                return;
            }
            
            const status: ETAStatus = {
                eta_seconds: Math.max(0, 30 - step * 3),
                current_step: step,
                total_steps: 10,
                tokens_used: step * 100,
                tokens_expected: 1000,
                elapsed_seconds: step * 3,
                progress_percent: step * 10,
                current_description: `Processing step ${step}`
            };
            
            this.handleStatusLine(`STATUS|${JSON.stringify(status)}`);
        }, 1000);
    }
    
    private handleStatusLine(line: string) {
        if (!this.enabled) return;
        
        // Parse STATUS| lines
        if (line.startsWith('STATUS|')) {
            const data = line.substring(7);
            
            if (data === 'COMPLETE') {
                this.handleComplete();
            } else {
                try {
                    const status = JSON.parse(data) as ETAStatus;
                    this.updateStatus(status);
                } catch (e) {
                    console.error('Failed to parse status:', e);
                }
            }
        }
    }
    
    private updateStatus(status: ETAStatus) {
        this.currentStatus = status;
        
        // Format status bar text (keep it under 30 chars)
        const etaStr = this.formatTime(status.eta_seconds);
        const text = `$(clock) ETA ${etaStr} | ${status.current_step}/${status.total_steps}`;
        
        this.statusBar.text = text;
        
        // Update tooltip with more details
        const tooltip = new vscode.MarkdownString();
        tooltip.appendMarkdown(`**Cursor Agent Progress**\n\n`);
        tooltip.appendMarkdown(`- **ETA:** ${etaStr}\n`);
        tooltip.appendMarkdown(`- **Progress:** ${status.progress_percent}%\n`);
        tooltip.appendMarkdown(`- **Step:** ${status.current_step}/${status.total_steps}\n`);
        if (status.current_description) {
            tooltip.appendMarkdown(`- **Current:** ${status.current_description}\n`);
        }
        if (status.tokens_expected > 0) {
            tooltip.appendMarkdown(`- **Tokens:** ${status.tokens_used}/${status.tokens_expected}\n`);
        }
        tooltip.appendMarkdown(`- **Elapsed:** ${this.formatTime(status.elapsed_seconds)}\n`);
        
        this.statusBar.tooltip = tooltip;
        this.statusBar.show();
        
        // Clear any existing hide timer
        if (this.hideTimer) {
            clearTimeout(this.hideTimer);
            this.hideTimer = null;
        }
    }
    
    private handleComplete() {
        // Show completion status
        this.statusBar.text = '$(check) Done';
        this.statusBar.tooltip = 'Agent task completed';
        
        // Hide after delay
        const config = vscode.workspace.getConfiguration('cursorETA');
        const hideDelay = config.get<number>('hideDelay', 5000);
        
        this.hideTimer = setTimeout(() => {
            this.statusBar.hide();
            this.currentStatus = null;
        }, hideDelay);
    }
    
    private formatTime(seconds: number): string {
        if (seconds < 60) {
            return `${seconds}s`;
        } else if (seconds < 3600) {
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `${mins}m ${secs}s`;
        } else {
            const hours = Math.floor(seconds / 3600);
            const mins = Math.floor((seconds % 3600) / 60);
            return `${hours}h ${mins}m`;
        }
    }
    
    showDetails() {
        if (!this.currentStatus) {
            vscode.window.showInformationMessage('No active Cursor agent task');
            return;
        }
        
        // Show detailed progress in output channel
        const output = vscode.window.createOutputChannel('Cursor ETA Details');
        output.clear();
        output.appendLine('=== Cursor Agent Progress ===');
        output.appendLine(`ETA: ${this.formatTime(this.currentStatus.eta_seconds)}`);
        output.appendLine(`Progress: ${this.currentStatus.progress_percent}%`);
        output.appendLine(`Current Step: ${this.currentStatus.current_step}/${this.currentStatus.total_steps}`);
        if (this.currentStatus.current_description) {
            output.appendLine(`Description: ${this.currentStatus.current_description}`);
        }
        output.appendLine(`Elapsed: ${this.formatTime(this.currentStatus.elapsed_seconds)}`);
        if (this.currentStatus.tokens_expected > 0) {
            output.appendLine(`Tokens: ${this.currentStatus.tokens_used}/${this.currentStatus.tokens_expected}`);
        }
        output.show();
    }
    
    toggle() {
        this.enabled = !this.enabled;
        if (this.enabled) {
            vscode.window.showInformationMessage('Cursor ETA Status enabled');
            if (this.currentStatus) {
                this.updateStatus(this.currentStatus);
            }
        } else {
            vscode.window.showInformationMessage('Cursor ETA Status disabled');
            this.statusBar.hide();
        }
        
        // Save preference
        vscode.workspace.getConfiguration('cursorETA').update('enabled', this.enabled, true);
    }
    
    private updateConfiguration() {
        const config = vscode.workspace.getConfiguration('cursorETA');
        this.enabled = config.get<boolean>('enabled', true);
        
        if (!this.enabled) {
            this.statusBar.hide();
        }
    }
}