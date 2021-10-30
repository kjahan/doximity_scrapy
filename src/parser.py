try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

class Parser:
    def __init__(self, html):
        self.parsed_html = BeautifulSoup(html, features="lxml")
        self.data = {}


    def parse(self):
        self.parse_basic_info()
        self.parse_educations()
        self.parse_similar_graph()


    def parse_basic_info(self):
    	# Extract basic info
    	self.data["first_name"] = self.parsed_html.body.find('span', attrs={'class':'user-name-first'}).text
    	self.data["middle_name"] = self.parsed_html.body.find('span', attrs={'class':'user-name-middle'}).text
    	self.data["maiden_name"] = self.parsed_html.body.find('span', attrs={'class':'user-name-maiden'}).text
    	self.data["last_name"] = self.parsed_html.body.find('span', attrs={'class':'user-name-last'}).text
    	self.data["credentials"] = self.parsed_html.body.find('span', attrs={'class':'user-name-credentials'}).text
    	self.data["profile_title"] = self.parsed_html.body.find('a', attrs={'class':'profile-head-subtitle'}).text

    	self.data["city"] = self.parsed_html.body.find('span', attrs={'itemprop':'addressLocality'}).text
    	self.data["state"] = self.parsed_html.body.find('span', attrs={'itemprop':'addressRegion'}).text

    	self.data["job_title"] = self.parsed_html.body.find('p', attrs={'class':'user-job-title'}).text

    	self.data["office_addr"] = self.parsed_html.body.find('span', attrs={'class':'black profile-contact-labels-wrap'}).text

    	div_phone_elem = self.parsed_html.body.find('div', attrs={'class':'profile-contact-labels-wrap'})
    	self.data["office_phone"] = div_phone_elem.find('span', attrs={'class':'black'}).text

    	div_fax_elem = self.parsed_html.body.find('div', attrs={'class':'office-info-fax'})
    	self.data["office_fax"] = div_fax_elem.find('span', attrs={'class':'black'}).text


    def parse_educations(self):
    	# Extract educations
    	educations = []

    	edu_section_elem = self.parsed_html.body.find('section', attrs={'class':'education-info'})
    	educations_items = edu_section_elem.find_all('li', attrs={'itemprop':'alumniOf'})

    	for li_item in educations_items:
    	    university_name = li_item.find('span', attrs={'class':'black'}).text
    	    job_pos = li_item.find('span', attrs={'class':'br'}).text
    	    educations.append({"university_name": university_name, "job_pos": job_pos})

    	self.data["educations"] = educations


    def parse_similar_graph(self):
    	# Exttract Graph (similar doctors)
    	similar_graph = []

    	similar_items = self.parsed_html.body.find_all('li', attrs={'class':'sidebar-pymk-list-item'})

    	for li_item in similar_items:
    	    similar_item_link = li_item.find('a')['href']
    	    similar_item_name = li_item.find('p', attrs={'class':'similar-profile-name'}).text
    	    span_items = li_item.find_all('span')
    	    
    	    attributes = []
    	    for span_item in span_items:
    	        if span_item.text:
    	            attributes.append(span_item.text)
    	    
    	    similar_graph.append({"link": similar_item_link, "name": similar_item_name, "field": attributes[0], "loc":  attributes[1]})

    	self.data["similar_graph"] = similar_graph


def run_parser():
    # Specialties --> https://www.doximity.com/directory/physicians
    # MichelleHanjani(Hanjani)GalantMD Dermatology • Redwood City, CA
    fn = 'logs/54d02a5326f7b844d1e0bb7e80257f7f.html'
    with open(fn,'rb') as infile:
        html = infile.read()
        parser = Parser(html)
        parser.parse()
        print(parser.data)


run_parser()
