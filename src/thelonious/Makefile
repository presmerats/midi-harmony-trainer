#!/bin/bash

# .PHONY: all clean

# SRC=$(wildcard *.ly)
# TGT=$(SRC:.ly=.pdf)

# all : ${TGT}

# %.pdf : %.ly
#     lilypond -o $@ $<

# clean :
# 	echo ${TGT}
#     #echo ${TGT} | rm




# try 02 ---------------------------------------------------------------
# # Basic wildcard usage
# # files_to_delete = $(wildcard *.o)
# #
# # clean:
# #   rm -f $(files_to_delete)
# midi_source_files=$(wildcard ./midi/*.mid)

# #SOME_PATH="--output=./lilys"

# .PHONY: links clean-links
# links: $(midi_source_files)

# # $(LINKS): %: $(SOME_PATH)/%
# #
# #foo.txt: $(SOME_PATH)/foo.txt
# #    ln -s $(SOME_PATH)/foo.txt
# # midi/Emajor_1octave.mid: $(SOMEPATH)/midi/Emajor_1octave.mid

# # source https://stackoverflow.com/questions/63288158/loop-through-files-in-make-file
# $(midi_source_files): %: "--output=./lilys"/$(%:.mid=.ly)
# 	@echo "$($@) $($<)"
# 	#midi2ly $@ $<

# # lily:
# # 	@echo running; \
# # 	echo "$(midi_source_files)";\
# #     echo "midi2ly $(midi_source_files) --output='./lilys/'"; \
# # 	echo "-------------------"; \
# # 	midi2ly $(midi_source_files)


# # HOw do wildcard rules work?
# # %.out: %.c
# #  gcc -o $* $*.c
# # ---
# # Now you can run make main.out, and it will create the main binary from the main.c file.
# %.pdf: %.ly
# 	lilypond -o $* $*.ly


# try 03 --------------------------------
# usage:
# $ make mysong01.pdf SONG_CONFIG=mysong01.yml
SONG_CONFIG="./mysong.yml"

%.mid:
	@echo           About to run midi_file_creator.py
	@echo "poetry run python midi_file_creator.py $(SONG_CONFIG) $(SONG_CONFIG:.yml=.mid) "
	@echo ""
	poetry run python midi_file_creator.py $(SONG_CONFIG) $(SONG_CONFIG:.yml=.mid)
	@echo ""
	@echo ""
	@echo ""

%.ly : %.mid
	@echo         About to create lilypond file from mid file
	#@echo "midi2ly $(SONG_CONFIG:.yml=.mid)  --output=$(SONG_CONFIG:.yml=.ly) "
	midi2ly $(SONG_CONFIG:.yml=.mid)  --output=$(SONG_CONFIG:.yml=.ly)
	@echo ""
	@echo ""
	@echo ""
	@echo         About to create lilypond file from _swing.mid file
	#@echo "midi2ly $(SONG_CONFIG:.yml=_swing.mid)  --output=$(SONG_CONFIG:.yml=_swing.ly) "
	midi2ly $(SONG_CONFIG:.yml=_swing.mid)  --output=$(SONG_CONFIG:.yml=_swing.ly)
	@echo ""
	@echo ""
	@echo ""


# %_swing.ly : %.mid
# 	@echo         About to create lilypond file from _swing.mid file
# 	#@echo "midi2ly $(SONG_CONFIG:.yml=_swing.mid)  --output=$(SONG_CONFIG:.yml=_swing.ly) "
# 	midi2ly $(SONG_CONFIG:.yml=_swing.mid)  --output=$(SONG_CONFIG:.yml=_swing.ly)
# 	@echo ""
# 	@echo ""
# 	@echo ""


%.pdf: %.ly
	@echo         About to create pdf file from lilypond file
	#@echo "lilypond -o $@ $<"
	lilypond -o $@ $<
	@echo ""
	@echo ""
	@echo ""
	@echo         About to create pdf file from lilypond _swing file
	#@echo "lilypond -o $(@:.pdf=_swing.pdf) $(<:.ly=_swing.ly)"
	lilypond -o $(@:.pdf=_swing.pdf) $(<:.ly=_swing.ly)
	@echo ""
	@echo ""
	@echo ""



# %_swing.pdf: %_swing.ly
# 	@echo         About to create pdf file from lilypond file
# 	@echo "lilypond -o $@ $<"
# 	lilypond -o $@ $<
# 	@echo ""
# 	@echo ""
# 	@echo ""

%.midi: %.pdf
	@echo         About to play the midi file
	fluidsynth -a coreaudio -n -i ../../external/FluidR3_GM.sf2 $(@:.midi=.pdf.midi)
