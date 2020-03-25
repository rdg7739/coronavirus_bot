import requests as rq
from bs4 import BeautifulSoup
import requests as rq
import telegram 
import os
    
class CoronaBot:
    def __init__(self):
        self.TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
        self.CHAT_ID = os.environ.get('CHAT_ID', '')
        self.DISPLAY_LIMIT = int(os.environ.get('DISPLAY_LIMIT', '10'))
        self.bot = telegram.Bot(token=self.TELEGRAM_TOKEN)
        if not self.TELEGRAM_TOKEN or not self.CHAT_ID:
            raise Exception('Need TELEGRAM_TOKEN, CHAT_ID')

    @staticmethod
    def run():
        BASE_URL = "https://google.org/crisisresponse/covid19-map"
        temp = CoronaBot()
        temp.getData(BASE_URL);
        
    def send(self, t):
        self.bot.sendMessage(self.CHAT_ID, t, parse_mode=telegram.ParseMode.HTML)
        
    def template(self, columns, data):
        body = []
        for i in range(1, data['count']):
            body.append([data[column][i] for column in columns])
        return '<code>' + '\n'.join(self.print_table(body, columns, 80, 6)) + '</code>'
    
    def getData(self, BASE_URL):
        res = rq.get(BASE_URL)
        soup = BeautifulSoup(res.content, 'html.parser')

        total = soup.select('.table_container thead th')
        columns = [str(column.text).replace(" ", "_") for  column in total]

        result = {}
        for column in columns:
            result[column] = [column.replace("_", " ")]
        result['count'] = 1

        table_rows = soup.select('.table_container tbody tr')
 
        for row in table_rows:
            tds = row.select('td')
            idx = 0
            for column in columns:
                result[column].append(tds[idx].text.strip())
                idx += 1
            result['count'] += 1
            if result['count'] > self.DISPLAY_LIMIT:
                break;

        data = self.template(columns, result)
        print(data)
        self.send(data)
        
    def pad (self, string, length=10, char=" "):
        string = str(string)

        if len(string) > length or len(char) > 1:
            return string

        strlen = len(string)
        padlen = abs(length - strlen)
        return string + (char * padlen)
   
    def print_table(self, lines, header=None, totalwidth=80, mincol=4, splitter=("|", "-", "+")):
        splitter, horiz, cross = splitter

        if splitter == "":
            splitter = " "
        if horiz == "":
            horiz = " "
        if cross == "":
            cross = " "

        width = {}
        total = {}
        average = {}
        fair_average = {}

        if header:
            col = 0
            for each in header:
                width[col] = len(each)
                col += 1

        num_lines = 0
        for line in lines:
            col = 0
            num_lines += 1
            for each in line:
                try:
                    if len(each) > width[col]:
                        width[col] = len(each)
                except:
                    width[col] = len(each)

                try:
                    total[col] += len(each)
                except:
                    total[col] = len(each)

                col += 1
        num_columns = col

        total_of_averages = 0
        for x in range(0,num_columns):
            average[x] = int( total[x]/num_lines )
            total_of_averages += average[x]

        total_of_widths = 0
        for x in range(0, num_columns):
            total_of_widths += width[x]

        amount_of_padding = (num_columns * len(splitter)) + len(splitter)

        if total_of_widths + amount_of_padding > totalwidth:

            for x in width:
                percent = float(average[x])/(total_of_averages)
                fair_average[x] = int((totalwidth - amount_of_padding) * percent)

            total_diff = 0
            for x in fair_average:
                if fair_average[x] < mincol:
                    difference = mincol - fair_average[x]
                    total_diff += difference
                    fair_average[x] = mincol

            if total_diff > 0:
                while total_diff > 0:
                    stole_some = False
                    for x in fair_average:
                        if fair_average[x] > mincol:
                            fair_average[x] -= 1
                            total_diff -= 1
                    if not stole_some:
                        break

            width = fair_average

        buffer = []
        if header:
            col = 0
            linebuffer = ""
            divider = ""
            for each in header:
                tmp=each
                if len(each) > width[col]:
                    tmp = each[0:width[col]]
                linebuffer += splitter + self.pad(tmp, width[col])
                divider += cross + horiz * width[col]
                col += 1
            linebuffer += splitter
            divider += cross
            buffer.append(linebuffer)
            buffer.append(divider)

        for line in lines:
            linebuffer = ""
            col = 0
            for each in line:
                tmp = each
                if len(each) > width[col]:
                    tmp = each[0:width[col]-2] + ".."

                linebuffer += splitter + self.pad(tmp, width[col])
                col += 1
            linebuffer += splitter
            buffer.append(linebuffer)

        return buffer