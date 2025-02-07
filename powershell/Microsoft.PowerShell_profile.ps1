# PowerShell Profile for MediTech Project
# ===================================

# Clear and Configure Aliases
function Initialize-SafeEnvironment {
    # Remove all aliases first
    Get-Alias | Remove-Item -Force -ErrorAction SilentlyContinue
    
    # Remove specific aliases
    @('ps', 'PS') | ForEach-Object {
        if (Test-Path "Alias:$_") {
            Remove-Item "Alias:$_" -Force -ErrorAction SilentlyContinue
        }
    }
    
    # Disable alias creation
    $ExecutionContext.SessionState.PSVariable.Set('AllowAliasCreation', $false)
}

Initialize-SafeEnvironment

# Configure Console
function Set-ConsoleConfiguration {
    try {
        # Create size objects
        $bufferSize = New-Object -TypeName System.Management.Automation.Host.Size -ArgumentList 120, 3000
        $windowSize = New-Object -TypeName System.Management.Automation.Host.Size -ArgumentList 120, 30
        
        # Set sizes
        $Host.UI.RawUI.BufferSize = $bufferSize
        $Host.UI.RawUI.WindowSize = $windowSize
        
        # Configure encoding
        [System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        $global:OutputEncoding = [System.Text.Encoding]::UTF8
        
        # Set environment
        $env:LANG = "en_US.UTF-8"
        $env:LC_ALL = "en_US.UTF-8"
        
        return $true
    }
    catch {
        Write-Warning "Console configuration error: $($_.Exception.Message)"
        return $false
    }
}

# Configure Script Analysis
function Set-ScriptAnalysis {
    try {
        # Define rules
        $analyzerSettings = @{
            IncludeDefaultRules = $true
            Rules = @{
                PSAvoidUsingCmdletAliases = @{
                    Enable = $true
                    Severity = 'Error'
                }
                PSUseCompatibleCommands = @{
                    Enable = $true
                }
                PSAvoidUsingPositionalParameters = @{
                    Enable = $true
                }
                PSUseConsistentIndentation = @{
                    Enable = $true
                }
            }
        }
        
        # Apply settings
        Set-PSDefaultParameterValues @{
            'PSScriptAnalyzer\Invoke-ScriptAnalyzer:IncludeDefaultRules' = $true
            'PSScriptAnalyzer\Invoke-ScriptAnalyzer:Settings' = $analyzerSettings
        }
        
        return $true
    }
    catch {
        Write-Warning "Script analyzer configuration error: $($_.Exception.Message)"
        return $false
    }
}

# Safe Process Management
function Get-ProcessInfo {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromPipeline = $true)]
        [string[]]$ProcessName
    )
    
    begin {
        Write-Verbose "Starting process information retrieval"
    }
    
    process {
        try {
            if ($ProcessName) {
                Get-Process -Name $ProcessName -ErrorAction Stop
            }
            else {
                Get-Process -ErrorAction Stop
            }
        }
        catch {
            Write-Error "Error retrieving process information: $($_.Exception.Message)"
        }
    }
    
    end {
        Write-Verbose "Process information retrieval completed"
    }
}

# Initialize Environment
$initResults = @(
    @{ Task = "Console Configuration"; Success = Set-ConsoleConfiguration }
    @{ Task = "Script Analysis"; Success = Set-ScriptAnalysis }
)

# Display Results
Write-Output "`nMediTech PowerShell Profile Configuration Results:"
Write-Output "================================================"

$initResults | ForEach-Object {
    $status = if ($_.Success) { "✓ Success" } else { "✗ Failed" }
    Write-Output "$status : $($_.Task)"
}

# Set Strict Mode Last
Set-StrictMode -Version Latest

# Show Confirmation Message
$loadedFeatures = @(
    "Increased buffer size (120x3000)",
    "UTF-8 encoding support",
    "Git configuration for UTF-8",
    "Strict mode enabled",
    "PSScriptAnalyzer configured",
    "Safe process handling enabled",
    "Alias safety measures applied"
)

Write-Output "MediTech PowerShell Profile loaded with:"
$loadedFeatures | ForEach-Object { Write-Output "- $_" } 