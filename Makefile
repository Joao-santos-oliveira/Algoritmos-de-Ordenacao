# ─── Detectar OS ─────────────────────────────────────────────────────────────
ifeq ($(OS), Windows_NT)
    DETECTED_OS := Windows
    EXT         := .exe
    RM          := del /Q /F
    MKDIR       := mkdir
    SLASH       := \\
else
    DETECTED_OS := Unix
    EXT         :=
    RM          := rm -f
    MKDIR       := mkdir -p
    SLASH       := /
endif

# ─── Diretórios ──────────────────────────────────────────────────────────────
DIR_C       = metodosOrdenacao/C
DIR_CPP     = metodosOrdenacao/CPP
DIR_GO      = metodosOrdenacao/GO
DIR_HS      = metodosOrdenacao/HASKELL
DIR_RS      = metodosOrdenacao/RUST
DIR_OUT     = builds

# ─── Binários de saída ───────────────────────────────────────────────────────
BIN_C       = $(DIR_OUT)/main_c$(EXT)
BIN_CPP     = $(DIR_OUT)/main_cpp$(EXT)
BIN_GO      = $(DIR_OUT)/main_go$(EXT)
BIN_HS 		= $(DIR_OUT)/HASKELL$(EXT)
BIN_RS      = $(DIR_OUT)/main_rs$(EXT)

# ─── C ───────────────────────────────────────────────────────────────────────
c:
	$(MKDIR) $(DIR_OUT)
	gcc $(DIR_C)/*.c \
	    $(DIR_C)/counting/*.c \
	    $(DIR_C)/introsort/*.c \
	    $(DIR_C)/radix/*.c \
	    -I$(DIR_C) \
	    -I$(DIR_C)/counting \
	    -I$(DIR_C)/introsort \
	    -I$(DIR_C)/radix \
	    -o $(BIN_C) -lm
	@echo "✔ C compilado -> $(BIN_C)"

c_run: c
	./$(BIN_C)

# ─── C++ ─────────────────────────────────────────────────────────────────────
cpp:
	$(MKDIR) $(DIR_OUT)
	g++ $(DIR_CPP)/*.cpp \
	    $(DIR_CPP)/counting/*.cpp \
	    $(DIR_CPP)/introsort/*.cpp \
	    $(DIR_CPP)/radix/*.cpp \
	    -I$(DIR_CPP) \
	    -I$(DIR_CPP)/counting \
	    -I$(DIR_CPP)/introsort \
	    -I$(DIR_CPP)/radix \
	    -o $(BIN_CPP)
	@echo "✔ C++ compilado -> $(BIN_CPP)"

cpp_run: cpp
	./$(BIN_CPP)

# ─── GO ──────────────────────────────────────────────────────────────────────
go:
	$(MKDIR) $(DIR_OUT)
	cd $(DIR_GO) && go build -o ../../$(BIN_GO) .
	@echo "✔ Go compilado -> $(BIN_GO)"

go_run: go
	./$(BIN_GO)

# ─── HASKELL ─────────────────────────────────────────────────────────────────
hs:
	$(MKDIR) $(DIR_OUT)
	cd $(DIR_HS) && cabal install --installdir=../../$(DIR_OUT) --overwrite-policy=always
	@echo "✔ Haskell compilado -> $(BIN_HS)"

hs_run: hs
	./$(BIN_HS)

# ─── RUST ────────────────────────────────────────────────────────────────────
rs:
	$(MKDIR) $(DIR_OUT)
	cd $(DIR_RS) && cargo build --release
	cp $(DIR_RS)/target/release/$(notdir $(DIR_RS))$(EXT) $(BIN_RS)
	@echo "✔ Rust compilado -> $(BIN_RS)"

rs_run: rs
	./$(BIN_RS)

# ─── Todos ───────────────────────────────────────────────────────────────────
all: c cpp go hs rs

# ─── Limpar ──────────────────────────────────────────────────────────────────
clean:
	$(RM) $(DIR_OUT)$(SLASH)*$(EXT)
	@echo "✔ outputs limpos"

.PHONY: c c_run cpp cpp_run go go_run hs hs_run rs rs_run all clean