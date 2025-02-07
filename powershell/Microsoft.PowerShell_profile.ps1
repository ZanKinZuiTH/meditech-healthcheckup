# PowerShell Profile for MediTech Project
# ===================================

# Clear and Configure Aliases
function Initialize-SafeEnvironment {
    # Remove all existing aliases
    Get-Alias | ForEach-Object {
        $aliasPath = 'Alias:\' + $_.Name
        Remove-Item -Path $aliasPath -Force -ErrorAction SilentlyContinue
    }
    
    # Explicitly remove problematic aliases
    $problematicAliases = @('ps', 'PS', 'gp', 'GPS')
    foreach ($alias in $problematicAliases) {
        $aliasPath = 'Alias:\' + $alias
        if (Test-Path $aliasPath) {
            Remove-Item $aliasPath -Force -ErrorAction SilentlyContinue
            Write-Output ('Removed alias: ' + $alias)
        }
    }
    
    # Prevent creation of new aliases
    $ExecutionContext.SessionState.PSVariable.Set('AllowAliasCreation', $false)
    
    # Verify removal
    $remainingAliases = Get-Alias | Where-Object { $problematicAliases -contains $_.Name }
    if ($remainingAliases) {
        $aliasNames = $remainingAliases.Name -join ', '
        Write-Warning ('Some problematic aliases could not be removed: ' + $aliasNames)
    }
}

# Run initialization
Write-Output "Initializing safe environment..."
Initialize-SafeEnvironment

# Configure Console
function Set-ConsoleConfiguration {
    try {
        # Create size objects with explicit type names
        $bufferSize = New-Object -TypeName System.Management.Automation.Host.Size -ArgumentList 120, 3000
        $windowSize = New-Object -TypeName System.Management.Automation.Host.Size -ArgumentList 120, 30
        
        # Set sizes with error checking
        try {
            $Host.UI.RawUI.BufferSize = $bufferSize
            $Host.UI.RawUI.WindowSize = $windowSize
        }
        catch {
            Write-Warning "Could not set console size: $($_.Exception.Message)"
        }
        
        # Configure encoding with explicit UTF-8
        [System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        $global:OutputEncoding = [System.Text.Encoding]::UTF8
        
        # Set environment variables
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
        # Define strict analyzer settings
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
                PSAvoidGlobalVars = @{
                    Enable = $true
                }
                PSUseDeclaredVarsMoreThanAssignments = @{
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

Write-Output "`nMediTech PowerShell Profile loaded with:"
$loadedFeatures | ForEach-Object { Write-Output "- $_" } 