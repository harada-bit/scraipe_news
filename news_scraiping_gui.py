import os,sys
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk
from time  import sleep

import news_scraiping_class as nsc


def gui_crate():

    root = tk.Tk()
    root.title("ニュース記事スクレイピングツール")
    root.minsize(300,200)

    """ 
    --------------------
    ボタンイベント関数
    --------------------
    """
 
    # スクレイピング処理
    def scraipe_kakunin(key,txw):
        scr = nsc.URL_SCR()
        element_list = scr.scraipe(key)
        i = 0
        txw.insert(float(i),element_list)
        return element_list

    def scraipe_hozon(key):
        scr = nsc.URL_SCR()
        element_list = scr.scraipe(key)
        return element_list

    # ファイル参照画面
    def dialog():
        iDir = os.path.abspath(os.path.dirname(__file__))
        filetypes = [("CSV", ".csv"), ("Text", ".txt")]
        iDir_Path = filedialog.asksaveasfilename(filetypes=filetypes,initialdir = iDir)
        return iDir_Path
        
    # テキストウィジェット表示
    def text_widget():
        root_text = tk.Tk()
        root_text.geometry("500x300")
        root_text.title('Webスクレイピングデータ内容')
        scr_text = tk.scrolledtext.ScrolledText(root_text)
        scr_text.pack()
        scr_text.configure(font=(8))
        return scr_text


    # 「実行」ボタンクリックのイベント
    def btn_jikko():
        # ウィンドウ表示
        # MEESAGE完了しました。
        tk.messagebox.showinfo('表示確認','表示内容を確認します。')
        # スクレイピング参照渡し[キーワード]
        txw = text_widget()
        tk.messagebox.showinfo('データ取得','データを取得致します。しばらくお待ち下さい。')
        element_list = scraipe_kakunin(textBox_key.get(),txw)
        tk.messagebox.showinfo('完了','完了しました')

    def btn_hozon():
        
        Messagebox = tk.messagebox.askquestion('ファイル保存','ファイルに保存しますか？')
        if Messagebox == 'yes':
            tk.messagebox.showinfo('ファイルの保存','保存先を選択して下さい')
            # ファイルダイアグラム参照
            path = dialog()
            tk.messagebox.showinfo('データ取得','データを取得致します。しばらくお待ち下さい。')
            df = scraipe_hozon(textBox_key.get())
            
            df.to_csv(path, encoding='utf_8_sig', index=False)

            # ファイル保存を参照渡し[ファイル名、パス名]
            # ファイル保存
            tk.messagebox.showinfo('完了','完了しました')
        else:
            tk.messagebox.showinfo('戻る','アプリケーション画面に戻ります')



    # 「閉じる」ボタンのイベント
    def btn_exit():
        Messagebox = tk.messagebox.askyesno('終了確認','画面を閉じてもよろしいでしょうか？')
        if Messagebox:
            tk.messagebox.showinfo('終了画面','アプリケーションを終了します')
            root.destroy()
        else:
            tk.messagebox.showinfo('戻る','アプリケーション画面に戻ります')

    """ 
    ---------------------
    WEbサイト設定フレーム
    ---------------------
     """


    # タイトルラベル
    LabelTitle = tk.Label(text="ニュース記事スクレイピングツール",font=("MSゴシック", "15", "bold"))
    LabelTitle.pack(anchor=tk.NW,padx=32,pady=30)

    # キーワードフレーム
    frame_site = tk.LabelFrame(
        root,
        borderwidth=1,
        relief="groove",
        text="キーワード設定",
        font=("MSゴシック", "12", "bold")
    )
    frame_site.pack(anchor=tk.W,padx=52, pady=(20,0))

    # キーワード入力
    textBox_key = tk.Entry(frame_site,width=50)
    textBox_key.pack(padx=52, pady=20)


    # 実行ボタンフレーム
    frame_button = tk.Frame()
    frame_button.pack(pady=20)
    
   # 実行ボタン
    Button_kakunin = tk.Button(frame_button,text="表示確認",width=10,command=btn_jikko)
    Button_kakunin.pack(side="left")
    Button_hozon = tk.Button(frame_button,text="ファイル保存",width=10,command=btn_hozon)
    Button_hozon.pack(side="left",padx=50)


    root.mainloop()


gui_crate()
