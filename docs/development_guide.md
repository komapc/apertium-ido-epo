# Apertium Ido–Esperanto Development Guide

## 🎯 **Mission Accomplished!**

This repository contains the Ido ↔ Esperanto language pair. The guide below focuses only on this pair and its build/test workflow.

## 📁 **Project Structure**

```
/home/mark/apertium-ido-epo/
├── lttoolbox/          # Core morphological processing library
├── apertium/           # Main Apertium translation engine
└── apertium-ido-epo/   # Ido–Esperanto language pair (this repo)
```

## 🔧 **Development Environment**

### **Core Tools (Installed to /usr/local/)**
- **lttoolbox** 3.0+ - Morphological processing library
- **apertium** 3.0+ - Translation engine and tools
- **VISL CG3** - Constraint grammar processor

### **Language Pair Status**
- ✅ **ido-epo** - Ido → Esperanto translation
- ✅ **epo-ido** - Esperanto → Ido translation

## 🚀 **Usage Examples**

### **Translation Commands**
```bash
# Ido to Esperanto
echo "me havas granda kato" | apertium ido-epo

# Esperanto to Ido
echo "mi havas grandan katon" | apertium epo-ido
```

### **Development Commands**
```bash
cd /home/mark/apertium-ido-epo/apertium-ido-epo
make

# Test with local changes
echo "Your text" | apertium -d . ido-epo

# List all available modes
apertium -l -d .
```

## 🛠 **Making Changes & Pull Requests**

### **Git Configuration**
- **Remote**: `https://github.com/komapc/apertium-ido-epo.git`
- **Working Directory**: `/home/mark/apertium-ido-epo/apertium-ido-epo/`

### **Development Workflow**
1. **Make Changes** to dictionary or transfer files:
   - `apertium-ido-epo.ido-epo.dix` - Bilingual dictionary
   - `apertium-ido-epo.ido-epo.t1x` - Transfer rules (ido→epo)
   - `apertium-ido-epo.epo-ido.t1x` - Transfer rules (epo→ido)

2. **Test Changes**:
   ```bash
   make
   echo "Test text" | apertium -d . ido-epo
   ```

3. **Submit Pull Request**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin your-branch-name
   ```

## 📚 **Key Files for Modification**

- **`apertium-ido-epo.ido-epo.dix`** - Main bilingual dictionary
- **`apertium-ido-epo.ido-epo.t1x`** - Ido→Esperanto transfer rules
- **`apertium-ido-epo.epo-ido.t1x`** - Esperanto→Ido transfer rules
- **`modes.xml`** - Translation pipeline configuration

## 🏗 **Build System**

Following the [official Apertium build instructions](https://wiki.apertium.org/wiki/Install_How_to_use_a_build):

- **`make langs`** - Build all language data
- **`make install`** - Install system-wide
- **`make clean`** - Clean build artifacts

## ✅ **Verification**

- ✅ Core tools compiled and installed from source
- ✅ Language pair builds successfully  
- ✅ Translation works both directions
- ✅ Development environment ready for PRs
- ✅ Following official Apertium procedures

## 🔗 **Resources**

- [Apertium Wiki](https://wiki.apertium.org)
- [Build Instructions](https://wiki.apertium.org/wiki/Install_How_to_use_a_build)
- [GitHub Repository](https://github.com/komapc/apertium-ido-epo)

**Environment Ready for Development!** 🎉
