#python 3.6.5
#python program to get updates of the corona virus pandemic


import requests
from bs4 import BeautifulSoup
import re,random
import smtplib
from time import ctime


class Covid():

    def user_agent(self):
        agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
         'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)']

        return {
            "User-Agent": agents[random.randint(0,len(agents)-1)]  #changing the user agent randomly each time the program runs to avoid being blocked
        }


    def pagination(self):
        url = 'https://www.worldometers.info/coronavirus/'       #website of corona virus stats
        response = requests.get(url,headers=Covid.user_agent(self))

        soup = BeautifulSoup(response.content,'html.parser')
        elements = soup.findAll(href=re.compile(r'.{0}country/.+/'))   #extacting country names to be used for pagination in case we want all the stats
        links = []
        i = 1

        for element in elements:
            href = element.attrs.get('href')
            links.append(href[8:len(href)-1])

        while links[i] != 'us':
            i=i+1

        pagination_keys = links[0:i-1]

        return(pagination_keys)    #country names


    def global_data(self):
        g_data = ['World','Total cases : ','Total deaths : ','Total recoveries : ']

        g_url = 'https://www.worldometers.info/coronavirus/'
        response = requests.get(g_url, headers=Covid.user_agent(self))

        soup = BeautifulSoup(response.content, 'html.parser')
        g_elements = soup.findAll('div', attrs={'class': 'maincounter-number'})   #extracting stats htmls

        for i in range(len(g_elements)):
              g_data[i+1] = g_data[i+1] + str(g_elements[i].span.text)  #parsing html stats

        return(g_data)


    def country_data(country):
        country = country
        c_data = [str(country),'Total cases : ','Total deaths : ','Total recoveries : ']

        c_url = 'https://www.worldometers.info/coronavirus/country/' + str(country) + '/'
        respose = requests.get(c_url, headers=Covid().user_agent())

        soup = BeautifulSoup(respose.content, 'html.parser')
        c_elements = soup.find_all('div', attrs={'class': 'maincounter-number'})

        for i in range(len(c_elements)):
            c_data[i+1] = c_data[i+1] + str(c_elements[i].span.text)


        update = soup.findAll('div', attrs={'class': 'news_body'})
        list = update[0].select('li.news_li')
        childlist = list[0].get_text()     #extracting the text which contains the new cases and deaths stats

        regex_cases = re.compile(r'\d+ new cases', re.IGNORECASE)   #extracting the numbers of new cases from the text
        regex_deaths = re.compile(r'\d+ new deaths', re.IGNORECASE)   #extracting the numbers of new deaths from the text

        item_case = regex_cases.findall(childlist)
        if len(item_case) == 0:
            item_case = 'no new cases'
            c_data.append(item_case)           #appending the new cases stats into the list

        item_death = regex_deaths.findall(childlist)
        if len(item_death) == 0:
            item_death = 'no new deaths'

        c_data.append(item_case)
        c_data.append(item_death)

        return(c_data)



    def send_mail(self,RECEIVER,gdata,cdata):
        SENDER = '*sender@gmail.com'
        PASS = '************'

        with smtplib.SMTP('smtp.gmail.com',587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(SENDER,PASS)

            subject = 'Corona virus stats '+str(ctime())   #ctime() returns the last update date
            body = str(gdata[0]) + '\n' +str(gdata[1])+'\n' +str(gdata[2])+ '\n' +str(gdata[3])+ '\n\n'\
                   + str(cdata[0]) + '\n' +str(cdata[1])+'\n' +str(cdata[2])+ '\n' +str(cdata[3]) +'\n' +str(cdata[4][0])+ '\n' +str(cdata[5][0])

            msg = 'Subject :{0} \n\n {1}'.format(subject,body)    #formatting the message

            smtp.sendmail(SENDER,RECEIVER,msg)
            print('email has been sent')



gdata = Covid().global_data()
cdata = Covid.country_data('algeria')
Covid().send_mail(*receiver,gdata,cdata)

#or extract all the data :
##################################
countries = Covid().pagination()
for country in countries:
    cdata = Covid.country_data(country)
    Covid().send_mail(*receiver, gdata, cdata)

###################################

# if you them in one messages , change the msg parameter in send_mail() to iterate each cdata for each country (by using pagination())







