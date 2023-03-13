# INSTALL TESSERACT IN YOU COMPUTER
from flet import *
import os
# INSTALL PYTESSERACT
import pytesseract
from PIL import Image as img
import re


def main(page:Page):
	page.scroll = "auto"

	# YOU IMAGE NAME IN YOU FOLDER PROJECT
	image_loc = TextField(label="you image name")
	id_number = TextField(label="id number")
	name_txt = TextField(label=" you name")
	birth_day = TextField(label="birth day")
	healthy_service = TextField(label="healthy service")

	# SEE YOU IMAGE FOR OCR
	image_preview = Image(src=False,width=150,height=120)


	def processyouimage(e):
		# GET IMAGE FOR PROCESS
		img_pro = img.open(image_loc.value)

		# AND GET TEXT IN YOU CARD IN MY LANGUANGE
		# MY LANGUAGE IS INDONESIA IF ENGLISH SET EN
		text = pytesseract.image_to_string(img_pro,lang="ind")
		# PRINT RESULT 
		print(text)

		# AND NOW RESULT TO WRITE TO FILE result.txt FILE
		# YOU RESULT in result.txt file
		with open("result.txt","w") as file:
			file.write(text)

		# AND AFTER WRITE GET result.txt file FOR PUSH 
		# TO TEXTFIELD WIDGET
		# THIS WILL AUTOMATICALY INPUT TEXT FROM YOU IMAGE UPLOAD
		with open("result.txt",mode="r",encoding="utf-8") as file:
			text = file.read()

		# AND NOW CREATE SECTION
		sections = {}
		lines = text.split("\n")
		current_section = ''

		i = 1
		for line in lines:
			if line.strip() == "":
				continue
				# IF SECTION ROW IS BLANK IN result.txt
				# THEN CONTINE
			# NOW FIND SECTION LIKE NAME BIRTHDAY AND MORE
			if "Tanggallahir" in line:
				current_section = "section_3"
				i += 1
			elif "NIK " in line:
				current_section = "section_4"
				i += 1
			elif "Faskes Tingkat " in line:
				current_section = "section_5"
				i += 1
			elif len(line.strip()) == 16 and line.strip().isdigit():
				current_section = "section_2"
				i += 1

			# AND IF SYSTEM FIND MANY TEXT IN YOU CARD
			# THEN CREATE NEXT SECTION 
			else:
				current_section = f"section_{i}"
			sections[current_section] = line.strip()
			i +=1
		print(sections)


		# AND NOW SET TEXTFIELD NAME birth_day and more
		# from sections
		id_number.value = sections['section_1']
		name_txt.value = sections['section_2']

		# GET dob
		dob = sections['section_3']

		# AND CREATE REGEX FOR FIND BIRTHDAY EXAMPLE 20-02-1099
		data_regex = re.compile(r'\d{2}-\d{2}-\d{4}')
		# AND FIND DOB FROM TEXT
		matches = data_regex.findall(dob)
		if matches:
			my_birthday = matches[0]
			# AND SET TEXTFIELD BIRTDAY 
			birth_day.value = my_birthday
		else:
			print("no dob found !!")

		healthy_service.value = sections['section_4']

		# AND NOW SET IMAGE PREVIEW OF YOU OCR CARD

		image_preview.src = f"{os.getcwd()}/{image_loc.value}"

		# AND SHOW SNACK BAR
		page.snack_bar = SnackBar(
			Text("success get from image",size=30),
			bgcolor="green"
			)
		page.snack_bar.open = True
		page.update()


	page.add(
		Column([
			image_loc,
			ElevatedButton("Process you image",
				bgcolor="blue",color="white",
				on_click=processyouimage
				),
			Text("YOu Result in image",weight="bold"),
			image_preview,
			id_number,
			name_txt,
			birth_day,
			healthy_service

			])


		)

flet.app(target=main)
