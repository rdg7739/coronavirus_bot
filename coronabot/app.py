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
        self.PICK_MY_COUNTRY = os.environ.get('PICK_MY_COUNTRY', '')
        if not self.TELEGRAM_TOKEN or not self.CHAT_ID:
            raise Exception('Need TELEGRAM_TOKEN, CHAT_ID')

    @staticmethod
    def run():
        BASE_URL = "https://news.google.com/covid19/map?hl=en-US&gl=US&ceid=US:en"
        temp = CoronaBot()
        temp.getData(BASE_URL);
        
    def send(self, t):
        self.bot.sendMessage(self.CHAT_ID, t, parse_mode=telegram.ParseMode.HTML)
        
    def template(self, columns, data):
        body = []
        for i in range(1, data['count']):
            for column in columns:
                temp = [column, data[column][i]]
                body.append(temp)
        return '<code>' + '\n'.join(self.print_table(body)) + '</code>'
    
    def getData(self, BASE_URL):
        # Set headers
        headers = rq.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        res = rq.get(BASE_URL, headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        total = soup.select('table thead th')
        columns = [str(column.text).replace(" ", "_") for  column in total ]
        result = {}
        for column in columns:
            result[column] = [column.replace("_", " ")]
        result['count'] = 1

        table_rows = soup.select('table tbody tr')
        print(len(table_rows))
        found_my_country = False
        for row in table_rows:
            th = row.select('th')[0]
            print(f"found_my_country {found_my_country} {self.PICK_MY_COUNTRY.strip().lower()} temp: {temp.lower()}" )
            if result['count'] <= self.DISPLAY_LIMIT or found_my_country:
                location_str = tds[0].text.strip()
                if self.PICK_MY_COUNTRY.strip().lower() in location_str.lower():
                    found_my_country = True
                result[columns[0].append(location_str)
                idx += 1
            if result['count'] > self.DISPLAY_LIMIT and found_my_country:
                break;
            tds = row.select('td')
            idx = 1
            temp = tds[idx].text.strip()
            for idx, column in enumerate(columns):
                if column.lower() == "location": 
                    continue
                temp = tds[idx].text.strip()
                result[column].append(temp)
                idx += 1
            result['count'] += 1

        result.pop('Cases_per_1M_people', None)
        print(result)
        columns.remove("Cases_per_1M_people")
        print(columns)
        data = self.template(columns, result)
        print(data)
        self.send(data)
        
    def pad (self, string, length=10, char=" "):
        string = str(string)

        if len(string) > length or len(char) > 1:
            return string

        strlen = len(string)
        padlen = abs(length - strlen)
        return (char * padlen) + string 
   
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
            divider = ""
            for each in line:
                tmp = each
                if len(each) > width[col]:
                    tmp = each[0:width[col]-2] + ".."
                linebuffer += splitter + self.pad(tmp, width[col])
                divider += cross + horiz * width[col]
                col += 1
            linebuffer += splitter
            buffer.append(linebuffer)
            if "Deaths" in line or "Location" in line:
                buffer.append(divider)

        return buffer
