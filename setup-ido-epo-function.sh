# Add this to your ~/.bashrc or ~/.zshrc for simple ido-epo translation
# Usage: echo "text" | ido-epo

ido-epo() {
    local input
    if [ -t 0 ]; then
        # No input from pipe, use arguments
        input="$*"
    else
        # Input from pipe
        input=$(cat)
    fi
    
    echo "$input" | bash -c 'cd /home/mark/apertium-dev/apertium/apertium-ido-epo && lt-proc ido-epo.automorf.bin | apertium-pretransfer | lt-proc -b ido-epo.autobil.bin | apertium-transfer -b apertium-ido-epo.ido-epo.t1x ido-epo.t1x.bin | lt-proc -g ido-epo.autogen.bin | lt-proc -p ido-epo.autopgen.bin'
}
