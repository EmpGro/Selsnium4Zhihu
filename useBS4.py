"用BS4代替正则表达式定位数据"
"解决card分三类用正则表达式不方便匹配的问题"
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag


def get_data(card):
	datlis = ['name', 'fuc', 'title', 'author']
	name = card.find('a', class_='UserLink-link', attrs = {'data-za-detail-view-element_name':'User'}).string
	datlis[0] = name
	#name也可以通过card.find_all('span', class_='Feed-meta-item')[-1].previous_sibling.strings 然后列表化取首项
	gefuc = card.find_all('span', class_='Feed-meta-item')[-1].previous_sibling
	#gefuc的类型是generator 需要list
	if isinstance(gefuc, Tag):
		fuc = list(gefuc.strings)[-1]
		datlis[1] = fuc
	#这里根据card的类型进行区别对待
	type1 = card.find('div', class_='QuestionItem-title')
	type2 = card.find('div', itemprop='zhihu:question')
	if type1:
		title = type1.find('a').string
		datlis[2] = title
	elif type2:
		title = type2.find('a').string
		author = card.find('div', class_='AuthorInfo-content').find('div', class_='AuthorInfo-head').find('a')
		datlis[2] = title
		if isinstance(author,Tag):
			datlis[3] = author.string
	elif datlis[1] == '发表了文章':
		title = card.find('h2', class_='ContentItem-title').find('a').string
		author = name
		datlis[2] = title
		datlis[3] = author
	return datlis


def get_datas(html):
	soup = BeautifulSoup(html, 'lxml')
	cards = soup.find_all('div', class_='Card TopstoryItem TopstoryItem--experimentExpand TopstoryItem--experimentButton')
	for card in cards:
		datlis = get_data(card)
		yield {
			'name' : datlis[0],
			'fuc' : datlis[1],
			'title' : datlis[2],
			'author' : datlis[3]
		}



def write_to_file(item):
	with open('result2.txt', 'a+', encoding='utf-8') as f3:
		f3.write(str(item)+'\n')



def main():
	with open('html.txt', 'r', encoding='utf-8') as f:
		html = f.read()
	for item in get_datas(html):
		if item['fuc'] != 'fuc':
			write_to_file(item)

if __name__ == '__main__':
	main()


	

