import requests
import tkinter
import webbrowser
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import filedialog


e1 = ''
ly_flag = 0
flag = 0
jiexi_url = ''
Video_inf = {}
playing_num = 0
video_list = []

def main():
    global Video_inf,video_list
    textLyric.delete(0.0, END)  # Text清空
    Video_inf = f.search_video(e1.get())
    textLyric.insert(END, '《{}》共有以下节目：\n\n'.format(e1.get()))
    for i in Video_inf:
        i = str(i) + '\n\n'
        textLyric.insert(END, i)
    video_list = list(Video_inf.keys())
    url = 'http://api.3ewl.cc/qingfeng.php?url={}'.format(Video_inf[video_list[playing_num]])
    textLyric.insert(END, '正在播放{}'.format(video_list[playing_num]))
    webbrowser.open(url)

def adjust():
    global playing_num
    textLyric.delete(0.0, END)  # Text清空
    playing_num += 1
    main()
    

def Input_videoname():
    global e1
    frame = tkinter.Frame(master)
    frame.pack(side=tkinter.LEFT, fill=tkinter.Y)
    lv = tkinter.StringVar()
    listBox = tkinter.Listbox(frame, selectmode=tkinter.BROWSE,
                              width=30, height=30, bg="#FFFFFF", listvariable=lv)
    listBox.pack()
    e1 = Entry(frame, bg='#FFFFFF')
    e1.place(x=50, y=150)
    Word = e1.get()
    tkinter.Label(master, text="输入", fg='#000000',
                  bg="#FFFFFF").place(x=10, y=148)
    Button(master, text='播放',command=main).place(x=50, y=180)
    Button(master, text='下一集',command=adjust).place(x=140, y=180)

def Init():
    global textLyric
    frame = tkinter.Frame(master)
    frame.pack(side=tkinter.TOP, fill=tkinter.Y)
    S = tkinter.Scrollbar(frame)
    textLyric = tkinter.Text(frame, bg="#FFFFFF", height=50)
    S.pack(side=RIGHT, fill=Y)
    textLyric.pack(side=LEFT, fill=Y)
    S.config(command=textLyric.yview)
    textLyric.config(yscrollcommand=S.set)
    #adjust()

class f:
    def search_video(video_name):
        global flag
        video_inf = {}
        #video_name = input('Please input the video name you want to watch:')

        res = requests.get('http://www.soku.com/search_video/q_{}?f=1&kb=04113000yv41000__&_rp=1520389727245ZDGC1h'.format(video_name))

        #print(res.content.decode('utf-8'))
        
        soup = BeautifulSoup(res.content.decode('utf-8'),'lxml')

        base_name = soup.select('.base_name a')
        #print(i[0]['_log_ct']) #_log_ct 1为电视剧 2为电影 3为综艺 5为动漫
        #print(i[0]['_iku_showid'])
        #url = 'http://list.youku.com/show/id_z{}.html'.format(i[0]['_iku_showid'])
        #print(url)
        for i in range(len(base_name)):  # 定位到合理的位置
            ct = int(base_name[i]['_log_ct'])
            if ct == 1:
                try:
                    juji = soup.select('.s_items.site14 .clearfix li')
                    sid = juji[0].select('a')[0]['_log_sid']
                except:
                    juji = soup.select('.s_items.all.site19  .clearfix li')
                    sid = juji[0].select('a')[0]['_log_sid']
                    flag = 1
                #print(sid)
                #print(j)
                for k in range(len(juji)):
                    try:
                        url_sid = juji[k].select('a')[0]['_log_sid']
                        #print(url_sid)
                        if url_sid == sid:    
                            url = juji[k].select('a')[0]['href']
                            if flag == 0:
                                url = 'http:' + url
                            else:
                                url = url.replace('+src=soku','')
                            #print(url)
                            video_inf[k+1] = url
                            #print(video_inf[k])
                        else:
                            break
                    except:
                        pass

                break
            elif ct == 2:
                #print(video_inf)
                url = 'http:' + base_name[0]['href']
                video_inf[video_name] = url
            elif ct == 3:  #找到各期的链接和名称
                try:
                    juji = soup.select('.s_items.s_col.site14 .clearfix li')
                    sid = juji[0].select('a')[0]['_log_sid']
                except:
                    juji = soup.select('.s_items.s_col.site19 .clearfix li')
                    sid = juji[0].select('a')[0]['_log_sid']
                    flag = 1
                #print(sid)
                #print(j)
                for k in range(len(juji)):
                    try:
                        url_sid = juji[k].select('a')[0]['_log_sid']
                        #print(url_sid)
                        if url_sid == sid:    
                            url = juji[k].select('a')[0]['href']
                            #print(url)
                            if flag == 0:
                                url = 'http:' + url
                            else:
                                url = url.replace('+src=soku','')
                            title = juji[k].select('a')[0]['title']
                            video_inf[title] = url
                            #print(video_inf[title])
                        else:
                            break
                    except:
                        pass

                break
        #return i[0]['href']
        #print(video_inf)
        return video_inf

if __name__ == '__main__':
    master = tkinter.Tk()
    master.title('VideoPlayer')
    master.geometry("700x500+200+100")
    Input_videoname()
    Init()
    master.mainloop()
