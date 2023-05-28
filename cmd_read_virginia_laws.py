#!/bin/env python

"""Read information from: https://law.lis.virginia.gov/jsonapi/"""

#
# Administrative Code
# Title, Agency

from json_fetcher import JsonFetcher

OUTPUT_DIR = "generated"

fetcher = JsonFetcher()
title_records = fetcher.fetch("https://law.lis.virginia.gov/api/AdministrativeCodeGetTitleListOfJson/")

for title in title_records:
    title_number = title['TitleNumber']
    if title_number != '24':
        continue
    title_record = fetcher.fetch(f"https://law.lis.virginia.gov/api/AdministrativeCodeGetAgencyListOfJson/{title_number}")
    title_name = title_record['TitleName']
    agencies = title_record['AgencyList']
    for agency in agencies:
        agency_number = agency['AgencyNumber']
        agency_name = agency['AgencyName']
        agency_record = fetcher.fetch(f"https://law.lis.virginia.gov/api/AdministrativeCodeChapterListOfJson/{title_number}/{agency_number}")
        chapters = agency_record['AgencyList'][0]['ChapterList']
        for chapter in chapters:
            chapter_number = chapter['ChapterNumber']
            chapter_name = chapter['ChapterName']
            url = f"https://law.lis.virginia.gov/api/AdministrativeCodeGetSectionListOfJson/{title_number}/{agency_number}/{chapter_number}"
            chapter_record = fetcher.fetch(url)
            if not chapter_record:
                continue
            sections = chapter_record['AgencyList'][0]['ChapterList'][0]['Sections']
            for section in sections:
                part_number = section['PartNumber']
                part_name = section['PartName']
                section_number = section['SectionNumber']
                section_title = section['SectionTitle']
                section_record = fetcher.fetch(f"https://law.lis.virginia.gov/api/AdministrativeCodeGetSectionDetailsJson/{title_number}/{agency_number}/{chapter_number}/{section_number}/0/0")
                print(f"{fetcher.fetch_count}, {fetcher.fetch_error}, {fetcher.cache_hit_count}, {fetcher.cache_miss_count}")
                # html = section_record['AgencyList'][0]['ChapterList'][0]['Sections'][0]['Body']
                # soup = BeautifulSoup(html, 'html.parser')
                # data = {
                #     'title_number': title_number,
                #     'title_name': title_name,
                #     'agency_number': agency_number,
                #     'agency_name': agency_name,
                #     'chapter_number': chapter_number,
                #     'chapter_name': chapter_name,
                #     'part_number': part_number,
                #     'part_name': part_name,
                #     'section_number': section_number,
                #     'section_title': section_title,
                #     'text': soup.get_text(),
                # }

                # print(f"{document_count}: title-{title_number}|agency-{agency_number}|chapter-{chapter_number}|part-{part_number}|section-{section_number}")
                # document_count = document_count + 1
                # generated_file_name = f"title-{title_number}|agency-{agency_number}|chapter-{chapter_number}|part-{part_number}|section-{section_number}.json"
                # generated_file_spec = os.path.join(OUTPUT_DIR, generated_file_name)
                # with open(generated_file_spec, "w", encoding="utf8") as f:
                #     f.write(json.dumps(data, default=str, indent=2, sort_keys=True))
                #     f.write('\n')

print(f"fetch_count: {fetcher.fetch_count}")
print(f"fetch_error: {fetcher.fetch_error}")
print(f"cache_hit_count: {fetcher.cache_hit_count}")
print(f"cache_miss_count: {fetcher.cache_miss_count}")
