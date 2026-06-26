# Vim Cheat Sheet

## Modes
```bash
i        # insert before cursor          a   # append after cursor
I        # insert at line start          A   # append at line end
o        # open line below               O   # open line above
v        # visual (char)                 V   # visual (line)
Ctrl-v   # visual block                  Esc # back to normal mode
R        # replace mode (overtype)
```

## Motion
```bash
h j k l        # left down up right
w  b  e        # next word / back word / end of word
0  ^  $        # line start / first non-blank / line end
gg  G          # top of file / bottom of file
42G  :42       # go to line 42
{  }           # paragraph back / forward
Ctrl-d Ctrl-u  # half page down / up
Ctrl-f Ctrl-b  # full page down / up
%              # jump to matching ( [ {
f x  ;  ,      # find char x on line / repeat / repeat reverse
H M L          # top / middle / bottom of screen
```

## Editing
```bash
x        # delete char            dd  # delete (cut) line
dw  de   # delete word            D   # delete to end of line
cw  cc   # change word / line     C   # change to end of line
yy  yw   # yank (copy) line/word  p P # paste after / before
r x      # replace one char       ~   # toggle case
u        # undo                   Ctrl-r # redo
.        # repeat last change     J   # join line below
>>  <<   # indent / outdent line
3dd  5yy # counts work: delete 3 lines, yank 5 lines
ciw  ci" # change inner word / inner quotes (text objects)
di(  ya{ # delete inside () / yank around {}
```

## Search & replace
```bash
/pattern        # search forward        ?pattern  # search backward
n  N            # next / previous match
*  #            # search word under cursor fwd / back
:%s/old/new/g            # replace all in file
:%s/old/new/gc           # replace all, ask each (confirm)
:s/old/new/g             # replace all on current line
:5,20s/old/new/g         # replace in line range 5..20
:noh                     # clear search highlight
```

## Registers
```bash
"ayy       # yank line into register a
"ap        # paste from register a
"+y  "+p   # yank to / paste from system clipboard
"0p        # paste last yank (survives deletes)
:reg       # show all registers
```

## Macros
```bash
qa         # start recording into register a
q          # stop recording
@a         # play macro a
@@         # replay last macro
5@a        # play macro a 5 times
```

## Files, buffers, windows
```bash
:w         # save              :wq  ZZ   # save & quit
:q         # quit              :q!       # quit, discard changes
:e file    # open file         :e!       # reload from disk
:ls        # list buffers      :bn :bp   # next / prev buffer
:b name    # switch to buffer by name
:sp file   # horizontal split  :vsp file # vertical split
Ctrl-w w   # cycle windows     Ctrl-w hjkl # move between windows
:tabnew    # new tab           gt  gT    # next / prev tab
```

## Marks & misc
```bash
ma         # set mark a        `a        # jump to mark a
``         # jump back to previous position
:set nu    # line numbers      :set rnu  # relative numbers
:set paste # paste without auto-indent mangling
g;         # jump to last edit
:%!jq .    # filter whole buffer through an external command
```
