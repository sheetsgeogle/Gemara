import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import requests
import os
from io import BytesIO
from PIL import Image
import re

# Base64 encoded favicon
favicon_base64 = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAakAAAFUCAYAAACeIMOcAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAC5zSURBVHhe7Z2/q13Xtf31H6h/jcqUKgJu5SKkkUGEFMYQEMHEpLtg0hhDBG5URKDCmBA3lxgMEYIouBEBExVGqQyXQBqjwAWDkQMGIQtDuvsybs6y992ae585914/xtpnfGDA1497z9n7vu+bQ3OuOee6dCaEEEKQIpMSQghBi0xKCCEELTIpIYQQtMikhBBC0CKTEkIIQYtMSgghBC0yKSGEELTIpIQQQtAikxJCCEGLTEoIIQQtMikhhBC0yKSEEELQIpMSQghBi0xKCCEELTIpIYQQtMikhBBC0CKTEkIIQYtMSgghBC0yKSGEELTIpIQQQtBCbVJX33zz7NrR0bluvPvu2a3j43M9OjnZ/YSowZ2je2e/unbne+G//3Drk7NPjh/vfqIfrv3mTxd066PH53r0jy93P9GGk3/9+8Jz3bj1l++f7fTr57ufasfR7/924fnw33i247/+c/cT7bjz82vf65M7t8716Yd3z7758nT3E6JnaE3q5MmTs0uvvmoKhiXqce3y0dmPL731kvA/7wkYwaWf3jGFwNuSu3/+3HwuCGbQmss/e998NqglX/7z5Oyt/7tk6vjo5u6nRM/QmhSyJcugIGRYoh6WQSV9++y73U/xg2zJCrLQ1V//cfdTbYARWc8FIWtpjfVcSc9e/Gf3U/X54u+PTIOCkFmJ/qE1qeOHD02DSlLJrw5fnX5jmlNSTyU/lKasIJvUsuR383f//f/vxjNByGJaGgHKjdZzJbXM9B7fOzYNKkklv/6hNSmcPVnmlIRs6tmLF7ufFqX4/NEXpjkloeTXSzY1l61AyKZanf+g3Gg9UxJMrJVRzWWgSa0MHudPljklKZvqH1qTOnr/fdOchrp8/fq5mZ0+fbr7LZGbfSYFwaiQUbGb1T6TgpC14Odqm9U+k4Ku/OLD82ywtll5TAqCkdY2q3u/PTLNaaj3fnL17OThg91viN6gNSl09FnGNCUYltUJuCWhBFrbkNHFZxnTlN64+t55B+DbNz44/92hPr776bnptTIzjxEMBcPC70AIwDCviCJY3z8nGFZ6ttRpF1HEhPHz1jPMKT0bNP7usWBsS40XmZJlTJaOfnT5pS7AJJQN0YRRAxjm+PtzCJ9b6x1qshmTOiTBhGuVOqMm5RXMDKZV07AQMK2AWkoRrN8vqUjGAyOxPiO3lpQ0IyblEYwMXYFoyCgBzsis782tD35549x4v3v+bPfN/UJrUsiMrAAt/U83b9/e/aXKcuvmsWkyOQUjrGFWyD6s4FhCkW7Budb4Uoow19SRW/i7RYwKpmIF6RyCAeYO8rlNdZ+S6fbcQEJrUlZgli6qBijdWcaSW8isvjgpe55hBcVSQtbmxXvmk0soY0aonYFGBoStwJxTCPK5Smgox1nfUUN4D5QEe4TSpHDuYgVl6aJqtOHDPCxTKSE0YJQyKvzr3AqIpYQSmZcHj5+Yn1FKEQMFyG6szyklbNvwUKt0hgC/NqPC75fM+rwqkR2WhtKk5gZ5pR9Uw6QsMykpmGKJ0l/tbCWSDdQ680lC+S6C9Rkl5TXRuUHe3MIZzxrw+9bnttA7r1zpqsGC0qQefPaZGZSli9qiSUE4o8pNbZNibExIimR5wPqMkvKaVO3y2dLA3rLMN6WcZczSUJoU2q2toCxdVOl2dJTeLBOpIWy6yMncbrwSihz+1z7zQXnRS4umDq9J4YzFCsCltGQXIEuZzxIyqh5KfzKpjlUazyBvKeXOpmpnKxFqm1Qky6udgUKsJoWgHoWpzGcJZ1TsUJoU5oCsoCz9ILTolwZbJCwDqaHXrryze4o81Gyj9gbZRM3WeCjCvn2HJeT9+7UwgEgrN64LsT6DTXhOZihNSoO8+4W/UWlKDfJ6lbPkVzNb8XanJazPKKVo+3ntDBTymlTtmSMI50secN7DWuYbC8/JPEdFaVJXXn/dDMzSDzoEk8q5Yb2mSTE3JkSzvBYm5e0+RPnNCrol5Zk1wjkP9gVav88q5ru3KE3KCsrSReHcrjS1BnmnhBuAc2EFw1KKtJ/XPvOJ3k1V09yTvCZvBdvS8pgUAr71u+xizaboTAo76aygLF3UIZgUvj8XVjAsJebGhGiW18KkPCaPbMUKtKW1z6R6OYeyxJpN0ZmUBnl9wixZaaauja8lDPbmoHYbdaT9vHZrfMRAQe2mDsjzjDUHeYeaMymcQ1m/05MYsymZVKfa6iDvWDmona1EqH3mA8OOYH1GaXlMns2kENx7aZSYk6ecWRuZVKc6eeIfyFyKZRq1lYOaJsXemBDF+oyS8nYfMplUj40SU1oyC1YamVSnqoFlGrWVg5omFW0/r2lSKN1FsT6npLwmz2RSvTZKTIltXRKdSSFDsIKydFE1sEyjtnJQ80wq2phQ06SiWR6wPqekvH+/Vuc/Y5PCf1s/17NwJT8TdCYFdOHhvGrMSIGa13RMKRcoI1lBMbci7eeg5jUd0fZzUPuajshewRZzUsNhXtx8a/1M72Ir+VGalHb3zauWST16cGIaR03lolbGEu2eQ5NALQONZnmg9lqk06+f7755Py3avVFmBFvo5JsTU5cfpUkBXI9uBWjp1bOj92OrbdZQ4/r4OeUCZlAjK4i0nydqZVNRA03U2nu45Mys9nkQzAnaQiffnJAlskBrUuD44UOtSDJUY5B3CLahv33jA9NESisnMBBkEyUzl6Xg3AxNF9Zn5hAMOtp+PgR/t9IzU9HLGBMowdXqrkMnX4syY20xnUtRm1QC9yZheBXBuVehRJe01nhh3q2AYWGnHvb6WcKWiKQcw8AlbukFyCpQykLwnRPOcayAOhaML3KeMgeebU12BTPBs+NzlmR2c8DorL8bDAaNGWuyVQw2rwEGgnIcyoBoaBgKGRcW0q41mNxmiOfBcw01fmaodos7vo+FLkxqq8B4l1xLUmOQNxfYZA5Tw9UblgntE0yxJd6NEGuyFIslJgVzWlrSy0nKWK1nnFPuv+EUMLLaQR9mBNOBgeL7YahLQKkRpTh8VumSIwsyKQKQGVlmNKUag7wlQKZlGdGcWpuUJzNYmwFYRM+B8Jy5s6a1RIxqyXnUWkobFT4fplSyCQGGhUzL+v61giEyIJMi4e79+6YhWeqZj+9+aprRlFqaFP5lbwXUoZbMHnmInJsxGhTAM1nPa2npedQaYB5WcF4rZDm1u+NKZIfeu7NKI5MiwntW1TuR7eotTcpzHlWivBYp9SEDYTSohNdso/NlucgZ2HFTcOvWbZxlWc+2RPgsBmRSRKC13DKloWrNSJUExmMZkqWWJrUvwJbKoiKlPoYzqDnwN7Kee6xWRosuNitAR4SzIaaWbWRVOc6rkBEyIJMiwnM2tQWTAt5GilYm5clmSv3r35t9tCiRRfG8C8qVrVibeaAhguXsZkiOWS6cdTEgkyLCs1x3KyblHRJuZVKebKbEv/69pT4Ef+YyX8J69rHQYNGKNauNUCpc2qVXA2RU1nN7BQNmQCZFhGe5Ls6ttoC3gaKVSe3LAKLbzr14S30tA7sXlCKtZx+rVuu5xdJAjiyFMYMas3Z1FAMyKTIsYxprC3jPpVqYlCebKdF2DjzlsV6yKE8LeovW8yFLy30wt15Y06LOgEyKDMuUxtoC2CRhmdJYLUyKvauvhywKeJomlmxmz8kSk2LpevOyptWewYxlUmRYpjTWVrBMaawWJoV/3VsBdagSmYy31NdDFoVntJ59rJalPhDt7mM5p4mCTj3rffZJJiVewjKlsbDLcAtYpjQWrgupiWeAF+W2EnhKfT109AHPFR+tS30gWgrrqcw3ZGk2JZMSL2GZ0lg97e6bwzKlsbBKqSaeXX0l5qO8pb7WmYcXz0b31qU+gMzICs6WWFqyl4JhY+u95sQw/yWTIuLZixemKY21FZPy3Pxb26Q85yglTMpT6ms5TxShl1IfsALzlHrNohJYc2S915wYzt9kUkR45qSgrZiUZz1SbZOygulYJUzKU+prtTooSi+lPrSQW4HZEmaitkB0wFcmJS7gNSlc8bEF2EzKO9eTu0zlKfX10nYOPJvjGUp9kcyCae3RGqIlP5mUuIDXpHCJ4hZgMynv1RK5A6yn1NdLw0QPA7yJSPs582aJCNHhXplUJnCWg6suoJ4732RSLwvrk2rhvb49d7nPU+rrpWGip7M1b2cfso+tEClxQjKplcCQsDn88vXrF4J4r8ikXhZ+phae+Sgop0l5Sn29NEycfv3cfP6xSm3riOI9n9lKqS9hveOUZFILwY67m7dvmwEc6hWvScGYtwCbSVkB1VLOOSlP5sES1PfheReI4WwtMje0lVJfIjIbJpMKgiCOLeBW4B6qV7wmtZVN6L2aFJQr0HpKfchQ2PFmUSxna96mid5noywizRMyqQBzmdNYvSKTelmsJoUy3Vo8pb5S29Zz482icvzdcoDgawXlsdBosDW87w7JpAJ4MqikXvFceggdkklBtbCC6pRydPh5AnsPs1HeLIphNirhLXn1cB1HlEiHn0wqwCGYFBoirPcZ6+qbb+5+o2/YTMrbOAHlaGbY9329zEZ5tnRATNvbPU0T+Jktgs0Z1vtakkkFwGV/VsC21Ctek4K2AJtJeYNt0pqzIs8iW5bzmzk8JcsklrM1bxv2llrPh8ikCmEF6in1ikzK1len3+x+oyzeYd6kNV13KBdanzkUy/nNFMjyvNknk+F6r4xnCNAlkEkVwgrUlnq+Xl0mZavWnVKRrABaU/LzlPrY8RhtUolLIpfivVup94WyU0QGemVSTrzbwaGemwoiJoW/Se+wmZS3AWCoJSWsLZT6IobONoyMZbFWQB5ry1jva0km5cTbmg0diknhb9I7XpOqefFhpHkCWtLl13upD8bsme9KYupQxGCuFYzH2srW8ymsd7Ykk3Iik3pZh2RSNZfMeud9kmBqUfYZ4ZLPrAXOoZAZWc9tie1dvOcxKAluGeudLenSQyfe+SFIJtUPjCbluQtprEim4Cn15ZjBKoV3CW8SU9s5QGZgBeOxtjjEO8R6Z0sM53JdmFQkePdsUjfefdd8J0tbuFPKa1I1N6EvOZeKLJz1lPpYN55Hs0zGOS/vEO9WmyaAt+QJyaScHIpJ4dmtd7KEv0nveE0KP1eT6LkU5DWWHkt9MJqoQUFsWRSwArGlrS2VHeIteUIyKSeRvX0yqX5gNalIa3WSpxuvx1IfMsvIGdRQSzofS+INzlvdNJGImBTDWqguTCoSvGVS/eA1qWuX6/7v1Hu77Fj7gnJvpT4MK0e6+IZibKH3nkdtcfP5kIhJMSCTIiLynlu4U8prUlBtlgTnfYG5h1IfjBbmtKTkORRbFgW8V1Tc+22/McSDTKoAVpCe0qGYVM/vmYiYVK3VSIklZzDQVHBmLvXhzAkditHOvSkxZlHAexPv1jv7IlvQGZBJESGTmlatrROJ6IqkpKkAzVbqSxlTdKmuR4xZVGQVEEOzQEl6K3vSm9Tp06dmkJ6STKofIiZVc+tEwgrAHllmw1Dqw3PBLJc2QnjE1viRiGQPuFp+y6Ccab33WDIpJ5FtE9ChmNQW7pSKmFTNgd7E0pLfeG6qVakPGQ3KeHiPpQ0QETHORSUiV6ZvHe+sGMtVJTIpIi5fv26+05R6J2JSd47u7X6rHktLftBw63etUh8MAs9cOluaEuNcVMJ7HrX1zj7gXbDLsLcP0JvU3fv3zQA9pZ673qz3mVPvREwKP9uCpRnIsHxXqtTX2pSGwjuwZlGR86hDMCnrvS3JpJxEtk1APc8PWe8zp96JmNRrV97Z/VZdlpb8IGQWOUt9KN+xmNJYTJvOx0TOo1gCcykihn3y8MHut9pCb1KRbRPQIZlUyTul0PKNjrqSeuPqe6YhTakFSwd7IWRhnrbuqVIfvhsdeDDKfdlYS0V2F7Ygch619fZz763EEEuXI71JRZoJoEMyqdyb0L84+fLs7RsfmAbBoNqzUomSBpFKfcmQGLOkfcpxnlYS73kUlDMw47OQmaGEOJb13Wxi6XKUSRFhvc+ccpoUDMoyBiYh+2oBynZWcJZ4W84TkfIWlCswe6+oZxYL9CZlBec5yaSWwZxBJbUyKZwFWQH60MXcLJGInEdBOYiU1FjFtGRXJkWE9T5zynmnFJa4WsbApG+ffbd72vqU2MzQu4Zt9qxEzqPeeeXK7rfW4W3xZhZKkixQm9TJkydmcJ7TIZlUrnfFWY9lCmxqyZIbe7cs9jJfInIelSMwo1xofXZvYhnkBdQmFR3khXo1qZbvipVDlikwCZ2AramxtaEHobGjB6LnUThHWgvatq3P7k1MrfjUJnX88KEZnOckk4qDbQ6WMTCp1TDvEGQPVtA+JMGoGRfIWiDQWgF4SjkCs3cvHrtwrsYCtUkhCFvBeU6HZFK5tmtE55VaqMVapDFqoLhzPkzcC9FW7xyBeQvnURDTJnhqk0IQtoLznA7JpHLtKbRMgU0tFsxa5LpzqUcxb5WwsILvnNYG5u+ePzM/t0fhXVigNqnojBQkk4qBtm7LFNjU4qoOizVLZ3tWbwYFw7GC75zWzkgt+U5WMUFtUriOwgrOc5JJxUCGYpkCm1rNSFkwrygqod4MCkTPo6C1LPlORjG1nwNqk7IC8z4dkknluFOqhyFeqOWM1BisL7KC+dYEM+5hFsoiejaUY3i1l3VH+8TUfg5oTQrLU63AvE85B1xrssSkoLX0MMQLMYEtC1tuR4c5wYjZt0lMseRsKEf2YH1uj2JqPwe0JrU0aOP3egTmar3PPq2hh319EEP7+ZgttqOjKaSn7r0plswqrc0etnQexXJFR4LWpJYG7V5NCmVK6332aQ2fHD82TYFNjCa1lXZ0DOb2nDVZLJlVWps9RHcEMgtD0EzQmtTSoH1oJrXmTqlbN49NU2ATS/v5mDUXIrZUMqZehnKjLJlVWmtSkR2B7GKD1qSWzEhBh2ZSa963hyFeiNWkPLfusggLcrdsTImls0prZ6QiOwKZBYNng9aklsxIQTIpH+iWswyBUUzt52NYt6Oj+QGZHs6YtlTK28fSazLWmNRWlspCOfYX5obWpJbMSEEyKR+9DPFCzCa15nr5nEpX1SNbYr8ptyRLLxtcwxbuj0pi6+wDtCZlBWSPDs2klrbc9zLEC7HTIpuSKdngTigr+O7TGrZwC2/S2rJnCShNaumMFHRoJoXfWwI65ixDYBPmuNipsSople+w/UGmZLO07Lb2HGapMTKKaWdfgtKkYDRWQPZIJuXDMgRGMbafW+RclZSypFsfPT4vJx7SmdIalpbd1gzybmmpbK6biXNDaVLee6QuX79+3mCBTsC79+93a1Dg5u3b5jsOhXM6vC+MKb3v6dOnu0/wg6aJuUwKrelY6IqzoCQxz9Kbe2FuQ0PaevddSfa1gSNjgiHh3AWGhtLW2swBM0Vz65Aws4XvYSyj9QKlSVlZBYIzAnkKzmvmgxhJ3Yy5jMgLtk5gqBfGBOPC/1ssYy6bQnaEsytsqoCh9boTjxm0gUMwDZwTwYxgDrWGU/FdGOrFd+MZ2IZie4W23IcgXTpAC5ETnE3BiFJmJDMSYj2UJiWEEEIAmZQQQghaZFJCCCFokUkJIYSgRSYlhBCCFpmUEEIIWmRSQgghaJFJCSGEoEUmJYQQghaZlBBCCFpkUkIIIWiRSQkhhKBFJiWEEIIWmZQQQghaZFJCCCFokUkJIYSgRSYlhBCCFpmUEEIIWmRSQgghaJFJCSGEoEUmJYQQghaZlBBCCFpkUkIIIWiRSQkhhKBFJiWEEIIWmZQQQghaZFJCCCFokUkJIYSgRSYlhBCCFpmUEEIIWmRSQgghaJFJCSGEoEUmJYQQghaZlBBCCFpkUkIIIWiRSQkhhKBFJiWEEIIWmZQQQghaZFJCCCFokUkJIYSgRSYlhBCCltUm9eqlVyVJkiQpLA8yKUmSJKmJPMikJEmSpCbyoDMpIYQQtMikhBBC0CKTEkIIQYtMSgghBC0yKSGEELTIpIQQQtAikxJCCEGLTEoIIQQtMikhhBC0yKSEEELQIpMSQghBi0xKCCEELTIpIYQQtMikhBBC0CKTEkIIQYtMSgghBC0yKSGEELTIpIQQQtAikxJCCEGLTEoIIQQtMikhhBC0yKSEEELQIpMSQghBi0xKCCEELTIpIYQQtMikhBBC0CKTEkIIQYtMSgghBC0yKSGEELTIpIQQQtAikxJCCEGLTEoIIQQtMikhhBC0yKSEEELQIpMSQghBi0xKCCEELTIpIYQQtFCb1NU33zy7dnR0rhvvvnt26/j4XI9OTnY/IXJx5+fXvtcnd26d69MP75598+Xp7idEa6795k8XdOujx+d69I8vdz/RhpN//fvCc9249Zfvn+306+e7n2rH0e//duH58N94tuO//nP3E5zcObp39qtrd74X/vsPtz45++T48e4nDgNakzp58uTs0quvmoJhiXx8+c+Ts7f+75Kp46Obu58SLYERXPrpHVMIvC25++fPzeeCYAatufyz981ng5i5dvno7MeX3npJ+J8fErQmhWzJMigIGZbIxxd/f2QaFITMSrQH2ZIVZKGrv/7j7qfaACOyngtC1tIa67mSnr34z+6n+LAMKunbZ9/tfmr70JrU8cOHpkElqeSXj8f3jk2DSlLJrz0oTVlBNqllye/m7/77f6vGM0HIYloaAcqN1nMlMWR6Fl+dfmOaU9IhlfxoTQpnT5Y5JSGbevbixe6nxRpw/mSZU5KyqfbMZSsQsqlW5z8oN1rPlAQTa2VUcxloUuszPYvPH31hmlMSSn6Hkk3RmtTR+++b5jTU5evXz83s9OnT3W+JJdz77ZFpTkO995OrZycPH+x+Q9Rmn0lByFrwc7XNap9JQVd+8eF5NljbrDwmBcFImcxqn0lBMCpkVFs3K1qTQkefZUxTgmFZnYBbEkqgJQwZmZJlTJaOfnT5pS7AJJQN0YRRAxjm+PtzCJ9b6x0ieIxgKBgWfgdCAIZ5RRTB+v45wbDSs6VOu4giJoyft55hTunZoPF3jwVjK2G86OKzjGlKb1x977wD8O0bH5z/7lAf3/303PR6NbPNmNQhCSacs9QZMSmPYGToCkRDRglwRmZ9b2598Msb58b73fNnu29uBwKmFVBLKYL1+yUVyXhgJNZn5FbukmbUpLyCmcG0ejIsWpNCZmQFaOl/unn79u4vtR6YihWkcwgGmDvI5zbVfUqm27KBBNmHFRxLKNItONcaX0oR5po6cgt/t1xGdevmsWkyOQUj7MGsaE3KCszSReXCCsw5hSCfq4SGcpz1HTWE90BJsAVWUCwlZG1evGc+uYQyZoTaGWiuAWGU7ixjyS1kVl+c8DWODKE0KZy7WEFZuqgcbfi1SmcI8GszKvx+yazPqxLZ4Rz417kVEEsJJTIvDx4/MT+jlCIGCpDdWJ9TSti2kQOYh2UqJYQGDGajojSpuUFe6QflMKm5Qd7cwhnPGvD71ue20DuvXKnWYFE7W4lkA7XOfJJQvotgfUZJRU10CstMSgqmyFr6ozSpB599ZgZl6aJymFTt8tnSwN6yzDelnGXMOWqbFGNjQlIkywPWZ5RUryYF4YyKEUqTQru1FZSli8rRjo4zFisAl9KSXYAsZT5LyKhKl/7mduOVUOTwv/aZD8qLXlo0deQwKZTeLBOpIWy6YEMm1bFyUNukENSjMJX5LOGMqiS1s5UItU0qkuXVzkChHCblGeQtJcZsitKkMAdkBWXpB6FFPwctDCDSyo3rQqzPYBOesxQ126ijQbZmazwUYd++wxLKYVLYImEZSA29duWd3VPwQGlSGuTdL/yNclB75gjC+ZIHnPewlvnGwnOWmqOqma1Eu9OszyilaPt57QwUymFSpQZ5vWIr+VGa1JXXXzcDs/SDcpkUym9W0C0pz6wRznmwL9D6fVaVunurpkkxNyZEDaCFSUW7Dy1amxTbhnVKk7KCsnRROLfLgRVsS8tjUgj41u+yq0Q2ZQXDUoq0n9c+84neTVXT3JOiJm9Ra5B3SrgBmAk6k8JOOisoSxeVw6SQrViBtrT2mVQv51CWSmRTVjAsJebGhKgBtDCpHBsnWpsUvp8JOpPSIK9PmCVbS81B3qHmTArnUNbv9KSc2VTtNupI+3nt1viIgYLaTR1Q9Bktpq6NryUM9jIhk+pUvW2bGGrKpBDce2mUmJOnnOmldrYSofaZDww7gvUZpZVjwaxlHLXFhEyqU5088Q81TsFkUj02SkxpySzYFDVNir0xIYr1GSUV7T6cwjKN2mJCJtWpcsBkUr02Skwp17qkmiYVbT+vaVIo3UWxPqekoiY/hWUatcUEnUkhQ7CCsnRROWh1/jM2Kfy39XM9C1fy56DmmVS0MaGmSS0xAOtzSir695vCMo3aYoLOpIAuPJxXrhkp0GJOajjMi5tvrZ/pXTlLfigjWUExt6KdaTWv6Yi2n4Pa13RE9grOUfOajikxQWlS2t03r5wm1aLdG2VGsIVOvjnl6vKrlbFEO9PQJFDLQJdkKbXXIp1+/Xz3zet49ODENI6aYoLSpACuR7cCtPTq2dH7eQ5oE7XPg2BO0BY6+eaELDEHMIMaWcGSzrRa2dTS1u5aew+XnJnNUeP6+DkxQWtS4PjhQ61IMpRr28QQlOBqddehk69FmbG2cp1LARgIsomSmctScG6GpgvrM3MIBh1tPx+Cv1vpmakc65DGYBv62zc+ME2ktJigNqkE7k3C8CqCc69CiS5prfHCvEsBA0E5DmVANDQMhYwLC2nXGkxuM8Tz4LmGGj8zVLvFHd9XAmQVKGUh+M4J5zhWQB0LxpfrPAXPtia7gpng2fE5OWaOhsDorL8bDAaNGWuyVQw2lwSGhZ162OtnCVsiknIMAzPd0tuFSW0VGO+Sa0lyDPKuBUZWO+jDjGA6MFB8Pwx1CSg1ohSHzypdcmyJdyPEmizFYolJwZyWlvRykjJW6xnnlPtvuBZsMoep4eoNy4T2CabIgkyKAGRGlhlNKccgby5KGxU+H6ZU6hoMAMNCpmV9/1rBEFvhyQxKZADRcyA8Z+6saS0Ro8p9HpUbZFqWEc1JJiVe4u79+6YhWWIC5mEF57VCllPSmCxKZIfeu7Nyg3/ZWwF1qFzDp2Mi52aMBgXwTNbzWipxHpWbj+9+aprRlGRSwsR7VsVGzsCOm4Jrm9MYnGVZz7ZE+KwWeM6jSpTXIqU+ZCCMBpXwmm2Ozec1iGxXl0kJE7SWW6Y0VM4ZqVygi80K0BHhbChXy3YOkFXlOK9CRtiCfQG2VBYVKfUxnEHNgb+R9dxjMRvtEBiPZUiWZFLCxHM2xWhSazMPNES0PLuZIscsF866auPJZkr969+bffRQIvO8C8qVPeFtpJBJCRPPcl1Gk1qz2gilwqVdejVARmU9t1cw4Np4spkS//r3lvoQ/HvIPqxnHwsNFj3hHRKWSQkTz3JdnFuxsTSQI0thzKDGrF0dVZt9GUB027kXb6mvh8COUqT17GOxtZ7vw9tAIZMSk1jGNBYbS8t9MLdeWNOiXhNPNlNq8NRTHusli/K0oLO3nlt4z6VkUmISy5TGYmOJSbXqelvKmlb7mmbM3tXXS3nM0zSxZDN7a7BJwjKlsWRSYhLLlMZiI9rd1+KcJgfo1LPeZ59qmhT+dW8F1KFKZDLeUl8PWRSe0Xr2sXor9SUsUxpLJiUmsUxpLOwyZCJaCuupzDdkaTZV6309A7wot5XAU+rroaMPeK746LHUl7BMaSxcF8KCTIoMy5TGYtjdNwSZkRWcLbVoyc4Jho2t95pTrfkvz66+EvNR3lJfL5mHZ6N7j6W+hGVKY2GVEgsyKSKevXhhmtJYbCZlBeYp9ZpFJbDmyHqvOdU6f/Oco5QwKU+pr5d5oq2X+oDn5l+ZlDDxzElBTCaFFnIrMFvCTNQWiA741jIpK5iOVcKkPKW+XlYHbb3UBzzrkWRSwsRrUrjig4VIZsG09mgN0ZJfDZPyzvXkLlN5Sn29tJ0Dz+b4nkt9QCYlFuM1KVyiyEKk/Zx5s0SE6HBvDZPyXi2RO8B6Sn29NExsdYB3jEyqATjLwVUXEFvnW4QeTcrb2YfsYytESpxQDZPyXt+eu9znKfX1EtS3dLY2h8eksD6Jha5NCoaEzeGXr1+/EMR7pUeT8p7PbKXUl7DecUo1TMozHwXlNClPqa+XoH769XPz+ccqfU18DTwmhZ9hoUuTwo67m7dvmwEc6hWvScGYGYjMDW2l1JeIzIbVMCkroFrKOSflyTx6Ceqed4F6OVubQyZVEARxbAG3AvdQveI1KZZN6N6mid5noywizRNMJgXlCrSeUh8yFHa8WVQvZ2v7kEkVYi5zGqtXejMpBF8rKI+FRoOt4X13iM2kUKZbi6fUV2rbem68WVSOvxsDMqlCeDKopF7xXHoIsZiUt+TVw3UcUSIdfmwmlaPDzxPYe5iN8mZRvc9GDfGYFMSCTIoINERY7zPW1Tff3P1GWzxNE/iZLYLNGdb7WqphUt7GCShHM8O+7+tlNsqzpQPq7XLDOWRShcBlf1bAttQrXpOCWuNtw95S6/kQNpPyBtukNWdFnkW2PZzfeEqWST2crXmRSRXCCtRT6pWeTMp7ZXyNAN0CNpPyDvMmrem6Q7nQ+syh2M9vkOV5s8+tNEwkvCb11ek3u99oy+ZMivF6dS89mZT3bqXeF8pOERnorWFSkawAWlPy85T62PEYbVKJSyJb4jUpljulujAp73ZwiKWpYAkRk8LfpCVYFmsF5LG2jPW+lmqYlLcBYKglJawtlPoihr6FDRNjZFIF8LZmQ4diUvibtAKDuVYwHmsrW8+nsN7ZUq2SZ6R5AlrS5dd7qQ/G7JnvSuple3sEr0mxXHwokyKiF5PynsegJLhlrHe2VGsllHfeJwmmFmWfES75zFrgHAqZkfXclpjfZQ1ek2JZMtuFSXnnhyCZVHmQGVjBeKwtDvEOsd7ZUq1zOc9dSGNFMgVPqS/HDFYpvEt4k7bUdj5EJlWASPDu2aRuvPuu+U6WWt4p5R3i3WrTBPCWPKFaf4cl51KRhbOeUh/rxvNoltnLnNcSvCbFsgldJkUEnt16J0v4m7TCCsSWtrZUdoi35AnVNOvouRTkNZYeS30wmqhBQVvNooDXpPBzDHRhUpG9fTKpsniD81Y3TSQiJlVzLVSktTrJ043XY6kPmWXkDGqoJZ2PvSCTKkAkeMukyuI9j9ri5vMhEZOqifd22bH2BeXeSn0YVo508Q3F3kK/Fq9JXbvMEUtlUkRE3rPVnVLeKyru/bbf/z14YDUpsCQ47wvMPZT6YLQwpyUlz6G2nEUBr0lBDHRhUlaQntKhmFSr9/TexLv1zr7IFvTaLDmDgaaCM3OpD2dO6FCMdu5NaetZFIiYFMNqJJkUEewmFVkFVLNZoAXMZc/oiqSkqQDNVupLGVN0qa5HW8+iQMSkGLZO0JvU6dOnZpCekkyqHJHsAVfLbxmUM633HqvV2ZwVgD2yzIah1IfnglkubYTwiK3xoxQRk2LYOkFvUpFtE9ChmFSLO6UiV6ZvHe+sWKurSpaW/MZzU61KfchoUMbDeyxtgIhoy3NRYyImxTDQK5Mi4vL16+Y7Tak23vOorXf2Ae+C3Vp7+8YsLflBw63ftUp9MAg8c+lsaUpbnosaEzGpO0f3dr/VDnqTunv/vhmgp9Sq6y0H1vvMqSaR86hDMCnrvS21MimwNAMZlu9Klfpam9JQeIdDyaJAxKTws62hN6nItgmo5SaGtVjvM6eaRM6jWgbmGkQM++Thg91v1WdpyQ9CZpGz1IfyHYspjbXFTedzREzqtSvv7H6rHfQmFdk2AR2SSdW8UypyHrX19nPvrcRQyy7HpYO9ELIwT1v3VKkP340OPBjlvmyspSK7C2uAlm901JXUG1ffMw1pSq2hN6lIMwF0SCZVcxO69zwKyhmY8VnIzFBCHMv6bja17nIsaRCp1JcMiTFL2qcc52lr+eLky7O3b3xgGgSDWs9KyaSIsN5nTrVMKlLegnIFZu8V9cxqDcp2VnCWOFrOYVCWMTAJ2VdL6E3KCs5zkknlJ3IeBeUgUlJjFcOSXZwFWQH60MXSLMGcQSXJpPZgBec5HZJJ1bpTKnIe9c4rV3a/tQ5vizezUJJkoMRmht41bLNvCZa4WsbApG+ffbd72jZQm9TJkydmcJ7TIZlUrXeNnEflCMwoF1qf3ZtaDfKOWXJj75bFUOYDOOuxTIFNraE2qeggL9SrSbG+a/Q8CudIa0HbtvXZvYmpFb/G1oYehMYOFrByyDIFJqETsDXUJnX88KEZnOckk8oLAq0VgKeUIzB79+KxC+dqLCB7sIL2IQlGzbRAFtscLGNgkoZ594AgbAXnOR2SSdXYrhFt9c4RmLdwHgUxbYJXA8Wd82FiJqLzSi2ktUh7QBC2gvOcDsmkauwptILvnNYG5u+ePzM/t0fhXZjIdedSj2LcKmGZApu0YHYP0RkpSCaVDxiOFXzntHZGasl3soqNNUtnexajQaGt2zIFNumqjj3gOgorOM9JJpWP6HkUtJYl38kolvbzMcwrikqIdS8fMhTLFNjUekYKUJuUFZj36ZBMqvSdUtGzoRzDq72sO9onlvbzMVhfZAXzrQlmzDILZdHDEC/UekYK0JoUlqdagXmfag245maJSUGlWHI2lCN7sD63RzG1nw/BloUtt6PDnGDE7Fdv9DDECzFAa1JLgzZ+r0dgrtb77FMplswqrc0etnQe1fKKjn1ssR0dTSFs3XtT9LCvD2JoPwe0JrU0aPdqUihTWu+zT6VYMqu0NnuI7ghkFoagWdlKOzoGc3vImsZ8cvzYNAU2yaT2sDRoH5pJlbpTasms0lqTiuwIZBc7ay5EbKlkTExDuVFu3Tw2TYFNDO3ngPb/mpbMSEGHZlIl3nfprNLaGanIjkBmweDZ8dy6yyIsyO3dmIb0MMQLyaT2sGRGCpJJrWfpNRlrTGorS2WhHPsLa8C6HR3ND8j0cMbUWylvH+iWswyBUQzt54DWpJbMSEEyqfUsvWxwDVu4PyqJtbNvzJrr5XMqXVWPbInhptyS9DLEC8mk9mAFZI8OzaRKtNzjTigr+O7TGrZwC2/S2rJnTVpkU4dkSmN6GeKFWKA0qaUzUtChmRR+LydLy25rz2GWGiOj2Hb2zVFjVVIq32H7w6GZ0hh0zFmGwCbMcbFAaVIwGisgeySTWsfSstuaQd4tLZXNdTNxTXKuSkpZ0q2PHp+XE7d2prQWyxAYxdJ+DihNynuP1OXr188bLNAJePf+/W4NCty8fdt8x6FwTof3hTGl9z19+nT3CXnY1waOjAmGhHMXGBpKW2szB8wUza1DwswWvqenMlpPLL25F+Y2NKStdN+VAk0Tc5kUWtOx0BVnQUmC1KSsrALBGYE8BedS80GtSN2MNYxoDrSBQzANnBPBjGAOtYZT8V0Y6sV34xmYh2K3xFw2hewIZ1fYVAFDY96J1wvYOoGhXhgTjAv/b2FDW+5DkK4doIU4VHA2BSNKmZHMSLBAaVJCCCEEkEkJIYSgRSYlhBCCFpmUEEIIWmRSQgghaJFJCSGEoEUmJYQQghaZlBBCCFpkUkIIIWiRSQkhhKBFJiWEEIIWmZQQQghaZFJCCCFokUkJIYSgRSYlhBCCFpmUEEIIWmRSQgghaJFJCSGEoEUmJYQQghaZlBBCCFpkUkIIIWiRSQkhhKBFJiWEEIIWmZQQQghaZFJCCCFokUkJIYSgRSYlhBCCFpmUEEIIWmRSQgghaJFJCSGEoEUmJYQQghaZlBBCCFpkUkIIIWiRSQkhhKBFJiWEEIIWmZQQQghaZFJCCCFokUkJIYSgRSYlhBCCFpmUEEIIUs7O/h/MWnM0be4hiAAAAABJRU5ErkJggg=="
)

# Inject custom HTML to set the favicon
st.markdown(
    f"""
    <head>
        <link rel="icon" href="{favicon_base64}" type="image/png">
    </head>
    """,
    unsafe_allow_html=True
)

st.title("Mishnayos for Yahrtzeit")

# Full Hebrew Name input with placeholder
full_hebrew_name = st.text_input("Full Hebrew Name", placeholder="e.g. מנחם מענדל")

def is_hebrew(text):
    # Check if the text contains Hebrew characters
    return bool(re.search(r'[\u0590-\u05FF]', text))

def download_font(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

        # Save the font file
        with open(filename, "wb") as f:
            f.write(response.content)
    except requests.RequestException as e:
        st.error(f"Failed to download font: {e}")

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return BytesIO(response.content)
    except requests.RequestException as e:
        st.error(f"Failed to download image: {e}")
        return None

def reverse_hebrew(text):
    return text[::-1]

def get_dynamic_font_size(text, max_width, font_name):
    # Try different font sizes and see what fits within max_width
    font_size = 86
    while font_size > 10:
        c = canvas.Canvas(BytesIO(), pagesize=letter)
        c.setFont(font_name, font_size)
        text_width = c.stringWidth(text)
        if text_width < max_width:
            return font_size
        font_size -= 1
    return 10  # Minimum font size

def create_pdf(name):
    pdf_file = BytesIO()  # Use BytesIO to create an in-memory PDF
    font_path = "SBL_Hbrw (1).ttf"  # Use a relative path or an appropriate location
    try:
        if os.path.exists(font_path):
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            # Register the SBL Hebrew font
            pdfmetrics.registerFont(TTFont('SBL_Hebrew', font_path))

            # Draw the black text
            c.setFont("SBL_Hebrew", 41)
            black_text = "םשה תויתוא לש תינשמה יקרפ"
            c.drawCentredString(width / 2, height - 100, black_text)

            # Determine the maximum width for the Hebrew name text
            max_name_width = 0.9 * width  # Allow some margin

            # Determine the appropriate font size
            font_size = get_dynamic_font_size(reverse_hebrew(name), max_name_width, "SBL_Hebrew")
            c.setFont("SBL_Hebrew", font_size)
            c.setFillColor(HexColor("#be9a63"))

            # Draw the gold text adjusted upwards
            reversed_name = reverse_hebrew(name)
            c.drawCentredString(width / 2, height - 180, reversed_name)  # Adjusted y-coordinate

            # Download and draw the swirl border image
            image_url = "https://github.com/sheetsgeogle/Gemara/raw/main/test2.png"
            image_file = download_image(image_url)
            if image_file:
                image = Image.open(image_file).convert("RGBA")
                # Save the image temporarily to calculate size
                temp_image_path = "temp_swirl_border.png"
                image.save(temp_image_path)

                # Get the size of the image
                img_width, img_height = image.size

                # Determine scale to fit the image in the desired area while preserving aspect ratio
                max_width = 0.07 * width  # Increased size
                max_height = 0.02 * height  # Increased size
                aspect_ratio = img_width / img_height

                if img_width > max_width or img_height > max_height:
                    if max_width / aspect_ratio <= max_height:
                        img_width = max_width
                        img_height = max_width / aspect_ratio
                    else:
                        img_height = max_height
                        img_width = max_height * aspect_ratio
                else:
                    img_width = img_width
                    img_height = img_height

                # Draw the image on the PDF
                c.drawImage(temp_image_path, width / 2 - img_width / 2, height - 0.3 * height, width=img_width, height=img_height, mask='auto')

            # Save the PDF
            c.save()
            pdf_file.seek(0)  # Rewind the BytesIO object to the beginning
            return pdf_file
        else:
            st.error(f"Font file not found at {font_path}.")
            return None
    except Exception as e:
        st.error(f"An error occurred while creating the PDF: {e}")
        return None

# URL of the SBL Hebrew font on GitHub
font_url = "https://github.com/sheetsgeogle/Gemara/raw/main/SBL_Hbrw%20(1).ttf"
font_path = "SBL_Hbrw (1).ttf"  # Use a relative path or an appropriate location
download_font(font_url, font_path)

# Validate and generate PDF
if full_hebrew_name:
    if is_hebrew(full_hebrew_name):
        pdf_file = create_pdf(full_hebrew_name)
        if pdf_file:
            # Define the filename with "the name" before the Hebrew name
            file_name = f"Mishnayos for the name {full_hebrew_name}.pdf"
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name=file_name,
                mime="application/pdf"
            )
        else:
            st.error("Error generating the PDF.")
    else:
        st.error("Please enter a name in Hebrew.")
