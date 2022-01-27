# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrotten_movie.models import ScrottenMovie
from scrotten_member.models import ScrottenMember
from scrotten_movie_to_member.models import ScrottenMovieToMember
from decimal import Decimal

def clean_data(param, variable_name = ''):
    
    if variable_name == '' :
        return param
    
    elif variable_name == 'movie_gross_sales':
        if param is None:
            return 0

        param = param.strip().replace('$', '')
        
        base = 0
        if 'K' in param:
            base = 1000
        if 'M' in param:
            base = 1000000
        if 'B' in param:
            base = 1000000000

        param = param.strip().replace('K', '')
        param = param.strip().replace('M', '')
        param = param.strip().replace('B', '')

        param = Decimal(param) * base
        return param
    
    elif variable_name == 'movie_genre':
        if param is None:
            return ''

        return param
        
        
    elif variable_name == 'member_birth_year':
        if param is None:
            return 0

        if not param:
            return 0
        
        if [s for s in param if 'not available' in s.lower()]:
            return 0
        
        return int(param[0].replace(' ', '').replace('\n', '')[-4:])
    
    
    elif variable_name == 'member_gender':
        if param is None:
            return ''

        male_found = [s for s in param if ' his ' in s.lower()]
        female_found = [s for s in param if ' her ' in s.lower()]
        
        ### Old method does not account for straing array of summary information
        # male_found = param.find(' his ')
        # female_found = param.find(' her ') 
        
        if male_found and female_found: return 'unkown'
        elif male_found : return 'male'
        elif female_found: return 'female'
        else : return ''

    elif variable_name == 'movie_approval_percentage':
        if param is None:
            return 0

        return param
    
    
    elif variable_name == 'member_start_movie_year':
        if param is None:
            return 0

        if not param:
            return 0
        
        return int(param[-1][0:4])
    
    
    elif variable_name == 'member_end_movie_year':
        if param is None:
            return 0

        if not param:
            return 0
        
        return int(param[0][-4:])
    
    
    elif variable_name == 'member_start_tv_year':
        if param is None:
            return 0
        
        if not param:
            return 0

        return int(param[-1][0:4])
    
    
    elif variable_name == 'member_end_tv_year':
        if param is None:
            return 0

        if not param:
            return 0
        
        return int(param[0][-4:])
        
    else:
        return param

# Member Details

class ScrottenCrawlerPipeline(object):

    def process_item(self, item, spider):
        
        # Movie Processing Start
        movie_id = clean_data(item['movie_id'])
        movie_name = clean_data(item['movie_name'])
        movie_genre = clean_data(item['movie_genre'], 'movie_genre')
        movie_year = clean_data(item['movie_year'])
        movie_gross_sales = clean_data(item['movie_gross_sales'], 'movie_gross_sales')
        movie_approval_percentage = clean_data(item['movie_approval_percentage'], 'movie_approval_percentage')

        if not ScrottenMovie.objects.filter(movie_id=movie_id).exists():
            ScrottenMovie.objects.create(
                movie_id=movie_id,
                name=movie_name,
                genre=movie_genre,
                year=movie_year,
                gross_sales=movie_gross_sales,
                approval_percentage=movie_approval_percentage,
            )

        # Member Processing Start
        member_id = clean_data(item['member_id'])
        member_name = clean_data(item['member_name'])
        member_birth_year = clean_data(item['member_birth_year'], 'member_birth_year')

        member_gender = clean_data(item['member_gender'], 'member_gender')
        member_start_movie_year = clean_data(item['member_start_movie_year'], 'member_start_movie_year')
        member_end_movie_year = clean_data(item['member_end_movie_year'], 'member_end_movie_year')
        member_start_tv_year = clean_data(item['member_start_tv_year'], 'member_start_tv_year')
        member_end_tv_year = clean_data(item['member_end_tv_year'], 'member_end_tv_year')
        
        member_total_active_movie_year = member_end_movie_year - member_start_movie_year
        member_total_active_tv_year = member_end_tv_year - member_start_tv_year
        member_total_movie_count = clean_data(item['member_total_movie_count'])
        member_total_tv_count = clean_data(item['member_total_tv_count'])

        if not ScrottenMember.objects.filter(member_id=member_id).exists():
            ScrottenMember.objects.create(
                member_id=member_id,
                name=member_name,
                birth_year=member_birth_year,
                gender=member_gender,
                start_movie_year=member_start_movie_year,
                end_movie_year=member_end_movie_year,
                start_tv_year=member_start_tv_year,
                end_tv_year=member_end_tv_year,
                total_active_movie_year=member_total_active_movie_year,
                total_active_tv_year=member_total_active_tv_year,
                total_movie_count=member_total_movie_count,
                total_tv_count=member_total_tv_count,
            )

        # Link Table Processing Start
        if not ScrottenMovieToMember.objects.filter(id=(movie_id+"@"+member_id)).exists():
            ScrottenMovieToMember.objects.create(
                id=(movie_id+"@"+member_id),
                movie_id=movie_id,
                member_id=member_id,
            )
        
        return item
