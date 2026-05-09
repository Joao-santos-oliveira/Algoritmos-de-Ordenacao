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
DIR_BENCH   = benchmarks

# ─── Binários de saída ───────────────────────────────────────────────────────
BIN_C       = $(DIR_OUT)/main_c$(EXT)
BIN_CPP     = $(DIR_OUT)/main_cpp$(EXT)
BIN_GO      = $(DIR_OUT)/main_go$(EXT)
BIN_HS      = $(DIR_OUT)/HASKELL$(EXT)
BIN_RS      = $(DIR_OUT)/main_rs$(EXT)

# ─── Repetição ───────────────────────────────────────────────────────────────
TIMES ?= 1

define run_times
	@for i in $(shell seq 1 $(TIMES)); do \
		TS=$$(date +%Y%m%d_%H%M%S)_$$(cat /proc/sys/kernel/random/uuid | cut -c1-8); \
		echo "── Execução $$i de $(TIMES) ──"; \
		$(1); \
	done
endef

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

c_run:
	@test -f $(BIN_C) || (echo "⚠ Binário não encontrado, compilando..." && $(MAKE) c)
	$(call run_times, ./$(BIN_C))

c_benchmark:
	@test -f $(BIN_C) || (echo "⚠ Binário não encontrado, compilando..." && $(MAKE) c)
	@$(MKDIR) $(DIR_BENCH)
	$(call run_times, /usr/bin/time -v ./$(BIN_C) 2>$(DIR_BENCH)/benchmark_c_$$TS.txt && grep -E "Maximum resident|wall clock" $(DIR_BENCH)/benchmark_c_$$TS.txt)

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

cpp_run:
	@test -f $(BIN_CPP) || (echo "⚠ Binário não encontrado, compilando..." && $(MAKE) cpp)
	$(call run_times, ./$(BIN_CPP))

cpp_benchmark:
	@test -f $(BIN_CPP) || (echo "⚠ Binário não encontrado, compilando..." && $(MAKE) cpp)
	@$(MKDIR) $(DIR_BENCH)
	$(call run_times, /usr/bin/time -v ./$(BIN_CPP) 2>$(DIR_BENCH)/benchmark_cpp_$$TS.txt && grep -E "Maximum resident|wall clock" $(DIR_BENCH)/benchmark_cpp_$$TS.txt)

# ─── GO ──────────────────────────────────────────────────────────────────────
go:
	$(MKDIR) $(DIR_OUT)
	cd $(DIR_GO) && go build -o ../../$(BIN_GO) .
	@echo "✔ Go compilado -> $(BIN_GO)"

go_run:
	@test -f $(BIN_GO) || (echo "⚠ Binário não encontrado, compilando..." && $(MAKE) go)
	$(call run_times, ./$(BIN_GO))

go_benchmark:
	@test -f $(BIN_GO) || (echo "⚠ Binário não encontrado, compilando..." && $(MAKE) go)
	@$(MKDIR) $(DIR_BENCH)
	$(call run_times, /usr/bin/time -v ./$(BIN_GO) 2>$(DIR_BENCH)/benchmark_go_$$TS.txt && grep -E "Maximum resident|wall clock" $(DIR_BENCH)/benchmark_go_$$TS.txt)

# ─── HASKELL ─────────────────────────────────────────────────────────────────
hs:
	$(MKDIR) $(DIR_OUT)
	cd $(DIR_HS) && cabal install --installdir=../../$(DIR_OUT) --overwrite-policy=always
	@echo "✔ Haskell compilado -> $(BIN_HS)"

hs_run:
	@test -f $(BIN_HS) || (echo "⚠ Binário não encontrado, compilando..." && $(MAKE) hs)
	$(call run_times, ./$(BIN_HS))

hs_benchmark:
	@test -f $(BIN_HS) || (echo "⚠ Binário não encontrado, compilando..." && $(MAKE) hs)
	@$(MKDIR) $(DIR_BENCH)
	$(call run_times, ./$(BIN_HS) +RTS -s 2>$(DIR_BENCH)/benchmark_hs_$$TS.txt && grep -E "total memory in use|Productivity|elapsed" $(DIR_BENCH)/benchmark_hs_$$TS.txt)

# ─── RUST ────────────────────────────────────────────────────────────────────
rs:
	$(MKDIR) $(DIR_OUT)
	cd $(DIR_RS) && cargo build --release
	cp $(DIR_RS)/target/release/$(notdir $(DIR_RS))$(EXT) $(BIN_RS)
	@echo "✔ Rust compilado -> $(BIN_RS)"

rs_run:
	@test -f $(BIN_RS) || (echo "⚠ Binário não encontrado, compilando..." && $(MAKE) rs)
	$(call run_times, ./$(BIN_RS))

rs_benchmark:
	@test -f $(BIN_RS) || (echo "⚠ Binário não encontrado, compilando..." && $(MAKE) rs)
	@$(MKDIR) $(DIR_BENCH)
	$(call run_times, /usr/bin/time -v ./$(BIN_RS) 2>$(DIR_BENCH)/benchmark_rs_$$TS.txt && grep -E "Maximum resident|wall clock" $(DIR_BENCH)/benchmark_rs_$$TS.txt)

# ─── Todos ───────────────────────────────────────────────────────────────────
all: c cpp go hs rs
	@echo "✔ Todos os binários compilados"

# ─── Limpar ──────────────────────────────────────────────────────────────────
clean:
	$(RM) $(DIR_OUT)$(SLASH)*$(EXT)
	@echo "✔ builds limpos"

.PHONY: \
	c c_run c_benchmark \
	cpp cpp_run cpp_benchmark \
	go go_run go_benchmark \
	hs hs_run hs_benchmark \
	rs rs_run rs_benchmark \
	all run_all benchmark clean