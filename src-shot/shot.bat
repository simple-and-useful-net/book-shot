@echo off


python mouse_pos.py


REM ショット範囲は,pos.txtに書きます
REM top,left,width,heigh(0930,1614,0304,0140)
echo ショット範囲は pos.txtからリード


REM 引数が指定されているかを確認
set max_count=%~1
if "%max_count%"=="" (
    set max_count=3
)


REM 繰返し数と待ち秒数の指定
REM set max_count=3
set wait=1


chcp 65001 >nul

REM pos.txtから座標を読み込み
for /f "tokens=1,2,3,4 delims=," %%a in (pos.txt) do (
    set top=%%a
    set left=%%b
    set width=%%c
    set height=%%d
)

echo 範囲(top,left,width,heigh)= %top%,%left%,%width%,%height%
set count=1

:loop

rem timeout /t 5 >nul
rem mss -m 1 -o screenshot_%count%.png -c 0957,1637,0274,0117

timeout /t %wait% >nul
mss -m 1 -o screenshot_%count%.png -c %top%,%left%,%width%,%height%

set /a count+=1


REM 回数分、ループしたら終了
if %count% leq %max_count% goto loop

echo スクリーンショット終了（繰返数,待ち秒数は, max_count,waitを変数）
