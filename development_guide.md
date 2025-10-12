# Apertium Belarusian-Russian Development Environment

## 🎯 **Mission Accomplished!**

You now have a fully functional Apertium development environment following the official installation guidelines.

## 📁 **Project Structure**

```
/home/mark/apertium-dev/
├── lttoolbox/          # Core morphological processing library
├── apertium/           # Main Apertium translation engine  
└── apertium-bel-rus/   # Belarusian-Russian language pair
```

## 🔧 **Development Environment**

### **Core Tools (Installed to /usr/local/)**
- **lttoolbox** 3.0+ - Morphological processing library
- **apertium** 3.0+ - Translation engine and tools
- **VISL CG3** - Constraint grammar processor

### **Language Pair Status**
- ✅ **bel-rus** - Belarusian → Russian translation
- ✅ **rus-bel** - Russian → Belarusian translation

## 🚀 **Usage Examples**

### **Translation Commands**
```bash
# Russian to Belarusian
echo "Привет, мир!" | apertium rus-bel
# Output: *Привет, мір!

# Belarusian to Russian  
echo "Прывітанне, свет!" | apertium bel-rus
# Output: Приветствие, мир!

# Complex sentence
echo "Дом красного цвета" | apertium rus-bel
# Output: Дом чырвонага колеру
```

### **Development Commands**
```bash
# Rebuild after changes
cd /home/mark/apertium-dev/apertium-bel-rus
make langs

# Test with local changes
echo "Your text" | apertium -d . bel-rus

# List all available modes
apertium -l -d .
```

## 🛠 **Making Changes & Pull Requests**

### **Git Configuration**
- **Remote**: `https://github.com/apertium/apertium-bel-rus.git`
- **Working Directory**: `/home/mark/apertium-dev/apertium-bel-rus/`

### **Development Workflow**
1. **Make Changes** to dictionary or transfer files:
   - `apertium-bel-rus.bel-rus.dix` - Bilingual dictionary
   - `apertium-bel-rus.bel-rus.t1x` - Transfer rules (bel→rus)
   - `apertium-bel-rus.rus-bel.t1x` - Transfer rules (rus→bel)

2. **Test Changes**:
   ```bash
   make langs
   echo "Test text" | apertium -d . bel-rus
   ```

3. **Submit Pull Request**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin your-branch-name
   ```

## 📚 **Key Files for Modification**

- **`apertium-bel-rus.bel-rus.dix`** - Main bilingual dictionary (6.3MB)
- **`apertium-bel-rus.bel-rus.t1x`** - Bel→Rus transfer rules (17KB)
- **`apertium-bel-rus.rus-bel.t1x`** - Rus→Bel transfer rules (23KB)
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
- [GitHub Repository](https://github.com/apertium/apertium-bel-rus)

**Environment Ready for Development!** 🎉
