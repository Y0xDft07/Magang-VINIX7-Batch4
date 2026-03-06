#!/bin/bash

# ===================================================
# INSTALLASI TOOLS KEAMANAN SIber - KALI LINUX/UBUNTU
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
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Fungsi untuk print banner
print_banner() {
    clear
    echo -e "${CYAN}"
    echo '╔══════════════════════════════════════════════════════════════╗'
    echo '║         AUTO INSTALLER - TOOLS KEAMANAN SIBER                ║'
    echo '║              Tugas Modul 2 - Cyber Security                  ║'
    echo '║                  Yoga Arfiyanto                               ║'
    echo '╚══════════════════════════════════════════════════════════════╝'
    echo -e "${NC}"
}

# Fungsi untuk print progress
print_progress() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_section() {
    echo -e "\n${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  $1${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}\n"
}

# Fungsi untuk cek koneksi internet
check_internet() {
    print_info "Memeriksa koneksi internet..."
    if ping -c 1 google.com &> /dev/null; then
        print_progress "Koneksi internet tersedia"
        return 0
    else
        print_error "Tidak ada koneksi internet!"
        return 1
    fi
}

# Fungsi untuk update system
update_system() {
    print_section "UPDATE SYSTEM"
    print_info "Mengupdate package list..."
    sudo apt update -y
    print_progress "Package list updated"
    
    print_info "Mengupgrade packages..."
    sudo apt upgrade -y
    print_progress "System upgraded"
}

# Fungsi untuk install tools dasar
install_basic_tools() {
    print_section "INSTALL TOOLS DASAR"
    
    tools=(
        "wget"
        "curl"
        "git"
        "vim"
        "nano"
        "htop"
        "net-tools"
        "build-essential"
        "cmake"
        "p7zip-full"
        "unzip"
        "zip"
        "gcc"
        "g++"
        "make"
        "python3"
        "python3-pip"
        "python3-dev"
        "python3-venv"
    )
    
    for tool in "${tools[@]}"; do
        print_info "Installing $tool..."
        sudo apt install -y "$tool" &> /dev/null
        if [ $? -eq 0 ]; then
            print_progress "$tool installed"
        else
            print_error "Failed to install $tool"
        fi
    done
}

# Fungsi untuk install tools hacking utama
install_hacking_tools() {
    print_section "INSTALL TOOLS HACKING UTAMA"
    
    tools=(
        "hydra"
        "medusa"
        "john"
        "hashcat"
        "sqlmap"
        "nmap"
        "nikto"
        "burpsuite"
        "metasploit-framework"
        "wireshark"
        "aircrack-ng"
        "crunch"
        "fcrackzip"
        "ophcrack"
        "rainbowcrack"
        "ncrack"
        "thc-pptp-bruter"
        "patator"
        "cewl"
        "rsmangler"
        "wordlists"
        "seclists"
        "dirb"
        "gobuster"
        "wfuzz"
        "whatweb"
        "theharvester"
        "recon-ng"
        "maltego"
        "spiderfoot"
    )
    
    for tool in "${tools[@]}"; do
        print_info "Installing $tool..."
        sudo apt install -y "$tool" &> /dev/null
        if [ $? -eq 0 ]; then
            print_progress "$tool installed"
        else
            print_warning "Failed to install $tool (may need manual install)"
        fi
    done
}

# Fungsi untuk install tools tambahan
install_extra_tools() {
    print_section "INSTALL TOOLS TAMBAHAN"
    
    # THC-Hydra GUI
    print_info "Installing hydra-gtk..."
    sudo apt install -y hydra-gtk &> /dev/null
    
    # John the Ripper Jumbo
    print_info "Installing john-jumbo..."
    sudo apt install -y john-jumbo &> /dev/null
    
    # Hashcat utilities
    print_info "Installing hashcat-utils..."
    sudo apt install -y hashcat-utils &> /dev/null
    
    # Crunch untuk generate wordlist
    print_info "Installing crunch..."
    sudo apt install -y crunch &> /dev/null
    
    # CeWL untuk custom wordlist
    print_info "Installing cewl..."
    sudo apt install -y cewl &> /dev/null
}

# Fungsi untuk install Python packages
install_python_packages() {
    print_section "INSTALL PYTHON PACKAGES"
    
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
        "pyfiglet"
        "termcolor"
        "pwntools"
        "cryptography"
        "hashlib"
        "bcrypt"
        "pyOpenSSL"
        "dnspython"
        "whois"
        "python-whois"
        "faker"
        "fake-useragent"
        "stem"
        "socks"
        "pysocks"
    )
    
    for package in "${packages[@]}"; do
        print_info "Installing $package..."
        pip3 install --quiet "$package" &> /dev/null
        if [ $? -eq 0 ]; then
            print_progress "$package installed"
        else
            print_error "Failed to install $package"
        fi
    done
}

# Fungsi untuk install Cain & Abel (via Wine)
install_cain_abel() {
    print_section "INSTALL CAIN & ABEL (VIA WINE)"
    
    # Install Wine
    print_info "Installing Wine..."
    sudo dpkg --add-architecture i386
    sudo apt update -y
    sudo apt install -y wine wine32 wine64 &> /dev/null
    
    if [ $? -eq 0 ]; then
        print_progress "Wine installed"
        
        # Download Cain & Abel
        print_info "Downloading Cain & Abel..."
        cd /tmp
        wget -q "https://josh.rootbrain.com/cain/ca_setup.exe" -O ca_setup.exe
        
        if [ -f ca_setup.exe ]; then
            print_progress "Cain & Abel downloaded"
            print_info "To install Cain & Abel, run: wine /tmp/ca_setup.exe"
        else
            print_error "Failed to download Cain & Abel"
        fi
    else
        print_error "Failed to install Wine"
    fi
}

# Fungsi untuk download wordlists
download_wordlists() {
    print_section "DOWNLOAD WORDLISTS"
    
    cd ~/Modul2_YogaArfiyanto/wordlists
    
    # Wordlist Indonesia
    print_info "Downloading Indonesian wordlist..."
    wget -q "https://raw.githubusercontent.com/mychaelgo/indonesia-wordlist/master/indonesian.txt" -O indonesian.txt
    if [ -f indonesian.txt ]; then
        lines=$(wc -l < indonesian.txt)
        print_progress "Indonesian wordlist downloaded ($lines lines)"
    fi
    
    # Wordlist dari target
    print_info "Downloading target wordlists..."
    wget -q "https://target.rootbrain.com/web101/username.txt" -O username.txt
    wget -q "https://target.rootbrain.com/web101/passwords.txt" -O passwords.txt
    
    if [ -f username.txt ]; then
        lines=$(wc -l < username.txt)
        print_progress "Username list downloaded ($lines entries)"
    fi
    
    if [ -f passwords.txt ]; then
        lines=$(wc -l < passwords.txt)
        print_progress "Password list downloaded ($lines entries)"
    fi
    
    # Common wordlists
    print_info "Downloading common wordlists..."
    wget -q "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-100.txt" -O top100.txt
    wget -q "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt" -O top_users.txt
    
    print_progress "Additional wordlists downloaded"
}

# Fungsi untuk setup environment
setup_environment() {
    print_section "SETUP ENVIRONMENT"
    
    # Buat direktori yang diperlukan
    mkdir -p ~/Modul2_YogaArfiyanto/{tools,wordlists,hashes,scripts,modules,attacks,logs,screenshots,backups}
    
    # Set permissions
    chmod +x ~/Modul2_YogaArfiyanto/scripts/*.py 2>/dev/null
    
    # Buat alias
    echo "alias modul2='cd ~/Modul2_YogaArfiyanto && python3 scripts/05_master_controller.py'" >> ~/.bashrc
    
    print_progress "Environment setup complete"
}

# Fungsi untuk verifikasi instalasi
verify_installation() {
    print_section "VERIFIKASI INSTALASI"
    
    tools_to_check=(
        "hydra"
        "medusa"
        "john"
        "hashcat"
        "sqlmap"
        "nmap"
        "python3"
        "pip3"
    )
    
    for tool in "${tools_to_check[@]}"; do
        if command -v "$tool" &> /dev/null; then
            version=$($tool --version 2>&1 | head -n 1)
            print_progress "$tool: $version"
        else
            print_error "$tool: NOT INSTALLED"
        fi
    done
    
    # Cek Python packages
    print_info "\nPython Packages:"
    pip3 list | grep -E "requests|beautifulsoup4|colorama" | while read line; do
        print_progress "$line"
    done
}

# Fungsi untuk show menu
show_menu() {
    print_banner
    echo -e "${WHITE}Pilih opsi instalasi:${NC}"
    echo -e "${CYAN}1)${NC} Install Semua Tools (Lengkap)"
    echo -e "${CYAN}2)${NC} Install Tools Dasar + Hacking Tools"
    echo -e "${CYAN}3)${NC} Install Python Packages Only"
    echo -e "${CYAN}4)${NC} Download Wordlists Only"
    echo -e "${CYAN}5)${NC} Setup Environment Only"
    echo -e "${CYAN}6)${NC} Install Cain & Abel (via Wine)"
    echo -e "${CYAN}7)${NC} Verifikasi Instalasi"
    echo -e "${CYAN}8)${NC} Exit"
    echo ""
    read -p "Pilihan [1-8]: " choice
    
    case $choice in
        1)
            print_info "Instalasi Lengkap..."
            check_internet || exit 1
            update_system
            install_basic_tools
            install_hacking_tools
            install_extra_tools
            install_python_packages
            install_cain_abel
            download_wordlists
            setup_environment
            verify_installation
            ;;
        2)
            print_info "Instalasi Tools Dasar + Hacking..."
            check_internet || exit 1
            update_system
            install_basic_tools
            install_hacking_tools
            install_extra_tools
            install_python_packages
            download_wordlists
            setup_environment
            verify_installation
            ;;
        3)
            print_info "Instalasi Python Packages..."
            check_internet || exit 1
            install_python_packages
            ;;
        4)
            print_info "Download Wordlists..."
            check_internet || exit 1
            download_wordlists
            ;;
        5)
            print_info "Setup Environment..."
            setup_environment
            ;;
        6)
            print_info "Install Cain & Abel..."
            check_internet || exit 1
            install_cain_abel
            ;;
        7)
            verify_installation
            ;;
        8)
            print_info "Keluar..."
            exit 0
            ;;
        *)
            print_error "Pilihan tidak valid!"
            ;;
    esac
    
    echo ""
    read -p "Tekan Enter untuk kembali ke menu..."
    show_menu
}

# Main program
if [[ $EUID -ne 0 ]]; then
   print_error "Script ini harus dijalankan sebagai root (sudo)!"
   exit 1
fi

# Start
show_menu
