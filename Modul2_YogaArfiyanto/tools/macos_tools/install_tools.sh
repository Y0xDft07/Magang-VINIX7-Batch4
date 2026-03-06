#!/bin/bash

# ===================================================
# INSTALLASI TOOLS KEAMANAN SIBER - MACOS
# Untuk Tugas Modul 2 Cyber Security
# Author: Yoga Arfiyanto
# ===================================================

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

print_banner() {
    clear
    echo -e "${CYAN}"
    echo '╔══════════════════════════════════════════════════════════════╗'
    echo '║         AUTO INSTALLER - MACOS - KEAMANAN SIBER              ║'
    echo '║              Tugas Modul 2 - Cyber Security                  ║'
    echo '║                  Yoga Arfiyanto                               ║'
    echo '╚══════════════════════════════════════════════════════════════╝'
    echo -e "${NC}"
}

# Fungsi untuk cek dan install Homebrew
install_homebrew() {
    echo -e "${BLUE}[ℹ]${NC} Checking Homebrew..."
    
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}[⚠]${NC} Homebrew not found. Installing..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add to PATH
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        echo -e "${GREEN}[✓]${NC} Homebrew installed"
    fi
}

# Fungsi untuk install tools via Homebrew
install_brew_tools() {
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  INSTALL TOOLS VIA HOMEBREW${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    
    tools=(
        "python@3.11"
        "git"
        "wget"
        "curl"
        "nmap"
        "hydra"
        "john"
        "hashcat"
        "sqlmap"
        "medusa"
        "crunch"
        "fcrackzip"
    )
    
    for tool in "${tools[@]}"; do
        echo -e "${BLUE}[ℹ]${NC} Installing $tool..."
        brew install "$tool" &> /dev/null
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[✓]${NC} $tool installed"
        else
            echo -e "${RED}[✗]${NC} Failed to install $tool"
        fi
    done
}

# Fungsi untuk install Python packages
install_python_packages() {
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  INSTALL PYTHON PACKAGES${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    
    packages=(
        "requests"
        "beautifulsoup4"
        "colorama"
        "mechanize"
        "selenium"
        "pycryptodome"
        "passlib"
        "python-nmap"
        "paramiko"
        "scapy"
        "pandas"
        "matplotlib"
        "tabulate"
    )
    
    pip3 install --upgrade pip
    
    for package in "${packages[@]}"; do
        echo -e "${BLUE}[ℹ]${NC} Installing $package..."
        pip3 install "$package" --quiet &> /dev/null
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[✓]${NC} $package installed"
        else
            echo -e "${RED}[✗]${NC} Failed to install $package"
        fi
    done
}

# Fungsi untuk download wordlists
download_wordlists() {
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  DOWNLOAD WORDLISTS${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    
    cd ~/Modul2_YogaArfiyanto/wordlists || exit
    
    # Indonesian wordlist
    echo -e "${BLUE}[ℹ]${NC} Downloading Indonesian wordlist..."
    curl -L -o indonesian.txt "https://raw.githubusercontent.com/mychaelgo/indonesia-wordlist/master/indonesian.txt"
    lines=$(wc -l < indonesian.txt)
    echo -e "${GREEN}[✓]${NC} Indonesian wordlist downloaded ($lines lines)"
    
    # Target wordlists
    echo -e "${BLUE}[ℹ]${NC} Downloading target wordlists..."
    curl -L -o username.txt "https://target.rootbrain.com/web101/username.txt"
    curl -L -o passwords.txt "https://target.rootbrain.com/web101/passwords.txt"
    echo -e "${GREEN}[✓]${NC} Target wordlists downloaded"
    
    # Common wordlists
    echo -e "${BLUE}[ℹ]${NC} Downloading common wordlists..."
    curl -L -o top100.txt "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-100.txt"
    curl -L -o top_users.txt "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt"
    echo -e "${GREEN}[✓]${NC} Common wordlists downloaded"
}

# Fungsi untuk setup environment
setup_environment() {
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  SETUP ENVIRONMENT${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    
    # Buat direktori
    mkdir -p ~/Modul2_YogaArfiyanto/{tools,wordlists,hashes,scripts,modules,attacks,logs,screenshots,backups}
    mkdir -p ~/Modul2_YogaArfiyanto/attacks/{password_attack,live_cracking,sql_injection}
    mkdir -p ~/Modul2_YogaArfiyanto/screenshots/{01_installation,02_password_attack,03_live_cracking,04_sql_injection}
    
    echo -e "${GREEN}[✓]${NC} Directories created"
    
    # Set permissions
    chmod +x ~/Modul2_YogaArfiyanto/scripts/*.py 2>/dev/null
    
    # Buat alias
    echo "alias modul2='cd ~/Modul2_YogaArfiyanto && python3 scripts/05_master_controller.py'" >> ~/.zshrc
    
    echo -e "${GREEN}[✓]${NC} Environment setup complete"
}

# Fungsi untuk verifikasi
verify_installation() {
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  VERIFIKASI INSTALASI${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    
    tools=("python3" "pip3" "hydra" "john" "hashcat" "sqlmap" "nmap")
    
    for tool in "${tools[@]}"; do
        if command -v $tool &> /dev/null; then
            version=$($tool --version 2>&1 | head -n 1)
            echo -e "${GREEN}[✓]${NC} $tool: $version"
        else
            echo -e "${RED}[✗]${NC} $tool: NOT FOUND"
        fi
    done
}

# Main menu
show_menu() {
    print_banner
    echo -e "\n${CYAN}Pilih opsi instalasi:${NC}"
    echo "1) Install Semua Tools (Lengkap)"
    echo "2) Install Homebrew + Tools"
    echo "3) Install Python Packages Only"
    echo "4) Download Wordlists Only"
    echo "5) Setup Environment Only"
    echo "6) Verifikasi Instalasi"
    echo "7) Exit"
    echo ""
    read -p "Pilihan [1-7]: " choice
    
    case $choice in
        1)
            install_homebrew
            install_brew_tools
            install_python_packages
            download_wordlists
            setup_environment
            verify_installation
            ;;
        2)
            install_homebrew
            install_brew_tools
            ;;
        3)
            install_python_packages
            ;;
        4)
            download_wordlists
            ;;
        5)
            setup_environment
            ;;
        6)
            verify_installation
            ;;
        7)
            exit 0
            ;;
        *)
            echo -e "${RED}Pilihan tidak valid!${NC}"
            ;;
    esac
    
    echo ""
    read -p "Tekan Enter untuk kembali..."
    show_menu
}

# Start
show_menu
