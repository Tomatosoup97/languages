OCAMLBUILD=ocamlbuild

# Should we build native or bytecode by default?
BUILD=native
# BUILD=byte

all: lang

lang:
	$(OCAMLBUILD) -use-menhir -menhir "menhir --explain" -libs unix -I . interp/$@.$(BUILD)

clean:
	$(OCAMLBUILD) -clean

