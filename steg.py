from PIL import Image, ImageDraw
import random

def create_steganographic_image():
	host_file_name = raw_input('Please enter the name of the host image (must be a png image): ')
	host_file = Image.open(host_file_name)
	host_file = host_file.convert('RGB')
	transform = ImageDraw.Draw(host_file)

	hidden_image_name = raw_input('Please enter the name of the image you wish to hide within the host: ')
	hidden_image = Image.open(hidden_image_name)
	hidden_image = hidden_image.convert('RGB')

	#minimum size of the host_file that can store all the data of the image to be hidden
	minimum_size = hidden_image.width * hidden_image.height * 8

	if minimum_size > host_file.width*host_file.height:
		print "Sorry, the host image is too small to properly store all the data.  Please use either a larger host image or smaller image to be hidden"
		return

	key = raw_input('Please name the file to store metadata and your one-time pad: ')
	f = open(key,"w+")

	f.write(str(hidden_image.height) + "\n" + str(hidden_image.width) + "\n")
	height = 0
	width = 0

	for y in range(hidden_image.height):
		for x in range(hidden_image.width):
			rand = random.randint(0,255)
			f.write(str(rand)+"\n")
			binary_repr_red = "{0:08b}".format(abs(hidden_image.getpixel((x,y))[0]-rand))
			binary_repr_green = "{0:08b}".format(abs(hidden_image.getpixel((x,y))[1]))
			binary_repr_blue = "{0:08b}".format(abs(hidden_image.getpixel((x,y))[2]))
			print rand
			for i in range(8):
				r_bit = binary_repr_red[i]
				g_bit = binary_repr_green[i]
				b_bit = binary_repr_blue[i]

				host_pix = host_file.getpixel((width,height))
				h_pix_r = host_pix[0]
				h_pix_g = host_pix[1]
				h_pix_b = host_pix[2]

				#if number value is odd and I want to store a 1, do nothing
				#if number value is even and I want to store a 1, add 1
				#if number value is even and I want to store a 0, do nothing
				#if number value is odd and I want to store a 0, subtract 1

				if r_bit=='0':
					if h_pix_r%2:
						h_pix_r = h_pix_r-1
				else:
					if h_pix_r%2 == 0:
						h_pix_r = h_pix_r+1
				
				if g_bit=='0':
					if h_pix_g%2:
						h_pix_g = h_pix_g-1
				else:
					if h_pix_g%2 == 0:
						h_pix_g = h_pix_g+1
				
				if b_bit=='0':
					if h_pix_b%2:
						h_pix_b = h_pix_b-1
				else:
					if h_pix_b%2 == 0:
						h_pix_b = h_pix_b+1

				transform.point((width,height), (h_pix_r,h_pix_g,h_pix_b))
				width = width+1
				if width == host_file.width:
					width = 0
					height = height+1








	# for y in range(host_file.height):
	# 	for x in range(host_file.width):
	# 		ok = host_file.getpixel((x,y))
	# 		transform.point((x,y), (ok[0],ok[1],ok[2]))
	# 		print host_file.getpixel((x,y))[0]
	# 		binary_repr = "{0:08b}".format(host_file.getpixel((x,y))[0])
	# 		print binary_repr[0]
	# 		print type(binary_repr)
	target_file_name = raw_input('Choose a file name to save the created steganographic image: ')
	
	host_file.save(target_file_name,'PNG')

	# target_file_name = raw_input('Choose a file name to store the steganographic image')
	# for line in host_file:
		# print line
		# break

def decrypt_steganographic_image():

	#test png is 300*300
	steganographic_img = raw_input('Please input the name of the steganographic image: ')
	steg_img = Image.open(steganographic_img)
	steg_img = steg_img.convert('RGB')



	deciphered_image = Image.new('RGB',(300,233))
	draw = ImageDraw.Draw(deciphered_image)

	max_width = steg_img.width
	max_height = steg_img.height
	height = 0
	width = 0

	for y in range(deciphered_image.height):
		for x in range(deciphered_image.width):
			red_value = ''
			green_value = ''
			blue_value = ''
			for i in range(8):
				pix = steg_img.getpixel((width,height))
				if pix[0]%2:
					red_value+='1'
				else:
					red_value+='0'
				if pix[1]%2:
					green_value+='1'
				else:
					green_value+='0'
				if pix[2]%2:
					blue_value+='1'
				else:
					blue_value+='0'
				width=width+1
				if width == max_width:
					height = height+1
					width = 0
			draw.point((x,y),(int(red_value,2),int(green_value,2),int(blue_value,2)))

	deciphered_image.save('decrypted.png','PNG')



def main():
	# action = 's'
	# while action !='q':
	# 	action = raw_input('What would you like to do?\n Press [q] to quit, [e] to create a steganographic image, or [d] to decrypt a steganographic image')
	# 	if action == 'e':
	# 		create_steganographic_image()
	create_steganographic_image()
	# decrypt_steganographic_image()



if __name__ == "__main__":
	main()