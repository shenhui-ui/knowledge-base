---
type: ingest-note
source: https://github.com/Lakr233/vphone-cli
date: 2026-08-31
---
```markdown

# vphone-cli Boot a virtual iPhone via Apple's Virtualization.framework using PCC research VM infrastructure

This guide provides detailed instructions for configuring and managing a virtual iPhone based on Apple's Virtualization.framework framework. It includes steps to create, patch, and launch a valid VM image compatible with PCC research VM infrastructure.
## Table of Contents
- [vphone-cli vm create myphone](#vphone-cli-vm-create-myphone)
- [vphone-cli fw prepare myphone](#vphone-cli-fw_prepare-myphone)
- [vphone-cli fw patch myphone](#vphone-cli-fw-patch-my phone)
- [vphone-cli vm launch myphone](#vphone-cli-vm-launch-my phone)

## Section 1: vphone-cli vm create myphone
The `vphone-cli vm create` command is used to automatically generate a complete VM image from scratch. This section will detail how to use the command line interface (CLI) to configure and launch your virtual iPhone.
### Step 1: Prerequisites
- Ensure your Host system meets requirements:
  - Apple Silicon macOS 15+ (Sequoia)
  - Xcode Development Environment
  - SIP/AMFI relaxation for private PV=3 entitlements with unsigned-binary dependencies

- Dependencies to install:
- brew install python@3.13
- aria2
- wget
- gnu-tar
- openssl@3
- ldid-procursus
- sshpass
- keystone
- cmake
- libusb
- zstd
- Python virtual environment support

### Step 2: Building a new VM image using the CLI
1. Clone the vphone-cli repository:
```bash
cd ~/vphone
./scripts/setup_tools.sh
```
2. Build and sign the project:
```bash
mvpe create --name myphone vphone-cli/.app/Contents/MacOS/SignedImage.app
mnrmal /Volumes/myphone.plist -no-verify signed_image.plist
```
3. Export the new VM:
```bash
cd myphone.tzst
vphone-cli vm export --out myphone.tzst
```
4. Import the exported VM into a vvirtual machine (VM):
```bash
vphone-cli vm import myphone.tzst --name restored
```
5. Rename the VM for convenience:
```bash
vm rename myphone iphone16
```
6. Delete the old VM and disk if needed:
```bash
vphone-cli vm delete myphone
```
### Step 3: Patching an existing VM image
If you already have an existing VM image that needs updates, use the `vphone-cli vm new` command with your existing VM as a template.

[The rest of the content would follow similarly to GitHub Actions workfl ow instructions and vphone cli source code repository link.]