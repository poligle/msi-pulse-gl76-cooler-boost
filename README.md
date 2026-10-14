> [!CAUTION]
> **This repo is no longer maintained since its considered finished and it will not receive new commits.**

# MSI Pulse GL76 11UEK Cooler Boost toggle for Linux

Small Linux script to toggle **Cooler Boost** on an MSI Pulse GL76 11UEK by writing the Cooler Boost bit in the Embedded Controller (EC), enabling external binding.

Tested only on:

- Laptop: MSI Pulse GL76 11UEK
- Board: MS-17L1
- BIOS: E17L1IMS.306
- EC firmware: 17L1EMS1.102
- Distro: Linux Mint
- Kernel tested: 6.17.0-29-generic

## What this does

On this EC firmware, Cooler Boost was observed at:

```text
EC path: /sys/kernel/debug/ec/ec0/io
Offset:  0x98
Bit:     7
Mask:    0x80

OFF observed: 0x06
ON observed:  0x86
```

The script does **not** blindly write `0x06` or `0x86`. It preserves the other bits and only toggles bit 7:

```python
# Enable
new = old | 0x80

# Disable
new = old & ~0x80
```

## Warning

This writes directly to the laptop Embedded Controller.

Use only if you have verified that your EC firmware matches the tested firmware or you have independently confirmed the same offset/bit behavior.

Do **not** assume this is safe for other MSI models, other GL76 variants, or other EC firmware versions.

## Install

```bash
sudo install -m 0755 msi-cooler-toggle.py /usr/local/bin/msi-cooler-toggle
```

Enable EC write support:

```bash
sudo modprobe -r ec_sys 2>/dev/null || true
sudo modprobe ec_sys write_support=1
```

Test:

```bash
sudo /usr/local/bin/msi-cooler-toggle
```

## Optional: load `ec_sys` with write support at boot

```bash
echo "options ec_sys write_support=1" | sudo tee /etc/modprobe.d/ec_sys.conf
echo "ec_sys" | sudo tee /etc/modules-load.d/ec_sys.conf
```

## Optional: allow running without password

Use `visudo`:

```bash
sudo visudo -f /etc/sudoers.d/msi-cooler
```

Add:

```text
YOUR_USERNAME ALL=(root) NOPASSWD: /usr/local/bin/msi-cooler-toggle
```

Replace `YOUR_USERNAME` with your Linux username.

Then your desktop shortcut can run:

```bash
sudo /usr/local/bin/msi-cooler-toggle
```

## Bind to a key in Linux Mint

Go to:

```text
System Settings → Keyboard → Shortcuts → Custom Shortcuts
```

Add:

```text
Name: MSI Cooler Boost
Command: sudo /usr/local/bin/msi-cooler-toggle
```

Assign any key combination that your external keyboard actually sends to Linux.

## Verify your own EC before using on another firmware

With Cooler Boost off:

```bash
sudo od -An -tx1 -j $((0x98)) -N 1 /sys/kernel/debug/ec/ec0/io
```

Then turn Cooler Boost on using the internal laptop keyboard shortcut and read again:

```bash
sudo od -An -tx1 -j $((0x98)) -N 1 /sys/kernel/debug/ec/ec0/io
```

On the tested EC firmware:

```text
OFF: 06
ON:  86
```

## Background

`msi-ec` did not load on this machine because it reported:

```text
msi_ec: Your firmware version is not supported!
```

Manual EC dump comparison showed that offset `0x98` changed consistently between `0x06` and `0x86` when Cooler Boost was toggled with the internal keyboard shortcut.
