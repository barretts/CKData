# Barrett Sonntag
# 2011

import urllib2
import csv
import time
import sys

from BeautifulSoup import BeautifulSoup

csvFile = csv.writer(open('ckdata-'+str(time.time()).replace('.','')+'.csv', 'wb'), delimiter=',')
csvCategory0 = ''
csvCategory1 = ''
csvCategory2 = ''
csvBrand = ''

mainPage = urllib2.urlopen('url')
mainSoup = BeautifulSoup(mainPage)

categoryLists = mainSoup.findAll('div', { 'class' : 'category-list' })
categoryAnchors = []
for categoryList in categoryLists:
    for categoryAnchor in categoryList.findAll('a'):
        categoryAnchors.append(categoryAnchor)

for categoryAnchor in categoryAnchors:
    csvCategory0 = categoryAnchor.string
    print csvCategory0
    
    categoriesPage = urllib2.urlopen(categoryAnchor['href'])
    categoriesSoup = BeautifulSoup(categoriesPage)

    subcategoryAnchors = categoriesSoup.find(id='subcategories').findAll('li')
    for subcategoryAnchor in subcategoryAnchors:
        csvCategory1 = subcategoryAnchor.find('a').string
        print '\t'+csvCategory1
        categoryPage = urllib2.urlopen(categoryAnchor['href']+subcategoryAnchor.find('a')['href'])
        categorySoup = BeautifulSoup(categoryPage)
        brandFoodUrls = []
        brandHs = categorySoup.find(id='page-content').findAll('h3')
        for brandH in brandHs:
            currentBrand = brandH.string.split(': ')[1]
            for foodAnchor in brandH.nextSibling.nextSibling.findAll('a'):
                brandFoodUrls.append([currentBrand,foodAnchor.string,foodAnchor["href"]])
            if brandH.nextSibling.nextSibling.nextSibling.nextSibling['class'] == 'float-half':
                for foodAnchor in brandH.nextSibling.nextSibling.nextSibling.nextSibling.findAll('a'):
                    brandFoodUrls.append([currentBrand,foodAnchor.string,foodAnchor["href"]])

        for brandFoodUrl in brandFoodUrls:
            foodPage = urllib2.urlopen(brandFoodUrl[2])
            foodSoup = BeautifulSoup(foodPage)
            print '\t\t'+brandFoodUrl[0]+' '+brandFoodUrl[1]
            servingSize = foodSoup.find(id='amount')['value']+' '+foodSoup.find(id='units').find('option').string
            nuts = foodSoup.find(id='nutrient-facts')
            # calories ---------------------------
            if nuts.find(id='calories') == None:
                calories = ''
            else:
                calories = nuts.find(id='calories').string
            # kilojoules ---------------------------
            if nuts.find(id='kilojoules') == None:
                kilojoules = ''
            else:
                kilojoules = nuts.find(id='kilojoules').string
            # total_fat ---------------------------
            if nuts.find(id='total_fat') == None:
                total_fat = ''
            else:
                total_fat = nuts.find(id='total_fat').string
            # saturated_fatty_acids ---------------------------
            if nuts.find(id='saturated_fatty_acids') == None:
                saturated_fatty_acids = ''
            else:
                saturated_fatty_acids = nuts.find(id='saturated_fatty_acids').string
            # trans_fatty_acids ---------------------------
            if nuts.find(id='trans_fatty_acids') == None:
                trans_fatty_acids = ''
            else:
                trans_fatty_acids = nuts.find(id='trans_fatty_acids').string
            # cholesterol ---------------------------
            if nuts.find(id='cholesterol') == None:
                cholesterol = ''
            else:
                cholesterol = nuts.find(id='cholesterol').string
            # sodium ---------------------------
            if nuts.find(id='sodium') == None:
                sodium = ''
            else:
                sodium = nuts.find(id='sodium').string
            # total_carbohydrate ---------------------------
            if nuts.find(id='total_carbohydrate') == None:
                total_carbohydrate = ''
            else:
                total_carbohydrate = nuts.find(id='total_carbohydrate').string
            # fiber ---------------------------
            if nuts.find(id='fiber') == None:
                fiber = ''
            else:
                fiber = nuts.find(id='fiber').string
            # sugars ---------------------------
            if nuts.find(id='sugars') == None:
                sugars = ''
            else:
                sugars = nuts.find(id='sugars').string
            # protein ---------------------------
            if nuts.find(id='protein') == None:
                protein = ''
            else:
                protein = nuts.find(id='protein').string
            # calcium ---------------------------
            if nuts.find(id='calcium') == None:
                calcium = ''
            else:
                calcium = nuts.find(id='calcium').string

            csvFile.writerow([csvCategory0, csvCategory1, brandFoodUrl[0], brandFoodUrl[1], servingSize, calories, kilojoules, total_fat, saturated_fatty_acids, trans_fatty_acids, cholesterol, sodium, total_carbohydrate, fiber, sugars, protein, calcium])
