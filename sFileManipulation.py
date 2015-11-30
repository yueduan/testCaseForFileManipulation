import zipfile
import sys, os
import shutil
kilobytes = 1024
megabytes = kilobytes * 1024
passwd = 'mypassword'

originalFile = 'bigFile.txt'
txtFileExtension = '.txt'
zipFileExtension = '.zip'
#aggregatedFile = 'aggregatedFile.zip'

# this function encodes/decoes data using XOR
def xor_crypt_string(inputFile, processedFile, key, encode, decode):
	fileFrom = open(inputFile, "r+")
	fileTo = open(processedFile, "w")
	
	try:
		data = fileFrom.read();
		from itertools import izip, cycle
		import base64
		if decode:
			data = base64.decodestring(data)
		xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
		result = xored
		if encode:
			result = base64.encodestring(xored).strip()
		fileTo.write(result)
	finally:
		fileTo.close()
		fileFrom.close()



# this function splits one file to many files based on chunksize
def split(fromfile, todir, chunksize): 
	if not os.path.exists(todir): 
		os.mkdir(todir)
	else:
		for fname in os.listdir(todir):
			os.remove(os.path.join(todir, fname)) 
	
	dotPos = fromfile.find(".")
	fileBasename = ""
	if dotPos == -1:
		fileBasename = fromfile
	else:
		fileBasename = fromfile.substring[0:dosPos]
	
	partnum = 0
	input = open(fromfile, 'rb')                   # use binary mode on Windows
	while 1:                                       # eof=empty string from read
		chunk = input.read(chunksize)          # get next part <= chunksize
		if not chunk: break
		partnum  = partnum+1
		filename = os.path.join(todir, (fileBasename + 'part%04d' % partnum))
		fileobj  = open(filename, 'wb')
		fileobj.write(chunk)
		fileobj.close()              
	input.close()
	assert partnum <= 9999                         # join sort fails if 5 digits
	return partnum


# this function aggregates given files in 'fromdir' to one file
def join(fromdir, tofile):
	output = open(tofile, 'wb')
	parts  = os.listdir(fromdir)
	parts.sort()
	for filename in parts:
		filepath = os.path.join(fromdir, filename)
		fileobj  = open(filepath, 'rb')
 		while 1:
			filebytes = fileobj.read(megabytes)
			if not filebytes: break
			output.write(filebytes)
		fileobj.close()
	output.close()


def doZip(orig, zipped):
	print "		Zipping..."
	import zipfile
	zf = zipfile.ZipFile(zipped, mode='w')
	try:
		print '		adding ', orig, ' into zip'
		zf.write(orig)
	finally:
		zf.close()


def doUnzip(zipped):
	print "		Unzipping..."
	import zipfile
	zf = zipfile.ZipFile(zipped)
	#unzipped = 'unzipped' + orig
	#target = open(unzipped, 'w')
	try:
		zf.extractall()
		#data = zf.read(orig)
		#target.write(data)
	finally:
		zf.close()
		#target.close()

# test 1: zip/unzip a big file
def test1():
	test1File = "bigFile1"
	# copy orignal file to test1 file for testing
	shutil.copy(originalFile, test1File)
	zippedFile = test1File + zipFileExtension
	
	# zip file
	doZip(test1File, zippedFile)

	# unzip file
	doUnzip(zippedFile)

	# remove generated files
	os.remove(test1File)
	os.remove(zippedFile)	
		

# test 2: encrypt/decrypt a big file
def test2():
	test2File = "bigFile2"
	# copy orignal file to test2 file for testing
        shutil.copy(originalFile, test2File)
        encryptedFile = test2File + 'encrypted' + txtFileExtension
	
	# encode the file and output the encoded file
	print "		encoding and encrpyting file..."
	xor_crypt_string(test2File, encryptedFile, passwd, True, False)
	
	# decode the file and output the original test file
	print "		decrypting and decoding file..."
	xor_crypt_string(encryptedFile, test2File, passwd, False, True)
	
	# remove generated files
	os.remove(test2File)
	os.remove(encryptedFile)

# test 3: split/merge a big file. split limit is 5MB by default.
def test3():
	test3File = "bigFile3"
        # copy orignal file to test3 file for testing
        shutil.copy(originalFile, test3File)
	splitFileDir = 'splitFiles'
	
	# split file into a set of smaller files (5MB)
        try:
		parts = split(test3File, splitFileDir, 5 * megabytes)
        except:
		print 'Error during split:'
		print sys.exc_type, sys.exc_value
        else:
		print '		Split finished:', parts

	# aggregate file
	try:
		join(splitFileDir, test3File)
        except:
		print 'Error aggregating files:'
		print sys.exc_type, sys.exc_value
        else:
 		print '		Merge completed'

	# remove generated file and directory
	os.remove(test3File)
	shutil.rmtree(splitFileDir)

# Encrypt the file and zip it. Then unzip and decrpyt it.
def test4():
	test4File = "bigFile4"
        # copy orignal file to test4 file for testing
        shutil.copy(originalFile, test4File)
	zippedFile = test4File + zipFileExtension
	encryptedFile = test4File + 'encrypted' + txtFileExtension

	# encode the file and output the encoded file
	print "		encoding and encrpyting file..."
	xor_crypt_string(test4File, encryptedFile, passwd, True, False)

	# zip file
	doZip(encryptedFile, zippedFile)

	# unzip file
	doUnzip(zippedFile)
	
	# decode the file and output the original test file
	print "		decrypting and decoding file..."
	xor_crypt_string(encryptedFile, test4File, passwd, False, True)

	# remove generated files
	os.remove(test4File)
	os.remove(encryptedFile)
	os.remove(zippedFile)	


# Encrypt the file and split it into smaller files. Then merge back and decrypt.
def test5():
	test5File = "bigFile5"
        # copy orignal file to test5 file for testing
        shutil.copy(originalFile, test5File)
	encryptedFile = test5File + 'encrypted' + txtFileExtension
	splitFileDir = 'splitFiles'
	
	# encode the file and output the encoded file
	print "		encoding and encrpyting file..."
	xor_crypt_string(test5File, encryptedFile, passwd, True, False)

	# split file into a set of smaller files (5MB)
        try:
		parts = split(encryptedFile, splitFileDir, 5 * megabytes)
        except:
		print 'Error during split:'
		print sys.exc_type, sys.exc_value
        else:
		print '		Split finished:', parts

	# aggregate file
	try:
		join(splitFileDir, encryptedFile)
        except:
		print 'Error aggregating files:'
		print sys.exc_type, sys.exc_value
        else:
 		print '		Merge completed'

	# # decode the file and output the original test file
	print "		decrypting and decoding file..."
	xor_crypt_string(encryptedFile, test5File, passwd, False, True)

	# remove generated files
	os.remove(test5File)
	os.remove(encryptedFile)
	shutil.rmtree(splitFileDir)
	

# Zip the file and split it. Then merge back and unzip.
def test6():
	test6File = "bigFile6"
        # copy orignal file to test6 file for testing
        shutil.copy(originalFile, test6File)
	zippedFile = test6File + zipFileExtension
	splitFileDir = 'splitFiles'
	
	# zip file
	doZip(test6File, zippedFile)

	# split file into a set of smaller files (5MB)
        try:
		parts = split(zippedFile, splitFileDir, 5 * megabytes)
        except:
		print 'Error during split:'
		print sys.exc_type, sys.exc_value
        else:
		print '		Split finished:', parts

	# aggregate file
	try:
		join(splitFileDir, zippedFile)
        except:
		print 'Error aggregating files:'
		print sys.exc_type, sys.exc_value
        else:
 		print '		Merge completed'

	# unzip file
	doUnzip(zippedFile)

	# remove generated files
	os.remove(test6File)
	os.remove(zippedFile)
	shutil.rmtree(splitFileDir)
	

def test7():
	test7File = "bigFile7"
        # copy orignal file to test7 file for testing
        shutil.copy(originalFile, test7File)
	zippedFile = test7File + zipFileExtension
	splitFileDir = 'splitFiles'
	encryptedFile = test7File + 'encrypted' + txtFileExtension

	# encode the file and output the encoded file
	print "		encoding and encrpyting file..."
	xor_crypt_string(test7File, encryptedFile, passwd, True, False)

	# zip file
	doZip(encryptedFile, zippedFile)

	# split file into a set of smaller files (5MB)
        try:
		parts = split(zippedFile, splitFileDir, 5 * megabytes)
        except:
		print 'Error during split:'
		print sys.exc_type, sys.exc_value
        else:
		print '		Split finished:', parts

	# aggregate file
	try:
		join(splitFileDir, zippedFile)
        except:
		print 'Error aggregating files:'
		print sys.exc_type, sys.exc_value
        else:
 		print '		Merge completed'

	# unzip file
	doUnzip(zippedFile)
	
	# decode the file and output the original test file
	print "		decrypting and decoding file..."
	xor_crypt_string(encryptedFile, test7File, passwd, False, True)
	
	# remove generated files
	os.remove(test7File)
	os.remove(zippedFile)
	os.remove(encryptedFile)
	shutil.rmtree(splitFileDir)
	
if __name__ == '__main__':
	print "This script is useful to generate test cases for forwardtracking"
	print "Test cases currently include the combination of the following file/process manipulations"
	print "Test 1 Zip/Unzip: Zip and unzip a given big file"
	print "Test 2 Encrypt/Decrypt: Encrypt and decrypt a given big file"
	print "Test 3 Split/Merge: Split a given big file into multiple parts and merge back"
	print "Test 4 Encrypt and Zip/Unzip and Decrypt: Combination of test 1 and test 2"
	print "Test 5 Encrypt and Split/Merge and Decrypt: Combination of test 2 and test 3"
	print "Test 6 Zip and Split/Merge and Unzip: Combination of test 1 and test 3"
	print "Test 7 Encrypt, Zip & Split/Merge, Unzip and Decrypt: Combination of test 1, test 2 and test 3"
	
	

	print "\nDoing test 1..."
	test1()		

	print "\nDoing test 2..."
	test2()
	
	print "\nDoing test 3..."
	test3()

	print "\nDoing test 4..."
	test4()

	print "\nDoing test 5..."
	test5()

	print "\nDoing test 6..."
	test6()

	print "\nDoing test 7..."
	test7()
