Test cases generation for File Manipulation

To generate test cases for forward tracker, we use two methods for test case generation.

I. Automatic test case generation.
	a. This method is to mimic malcious activities since attackers normally move data automatically using scripts other than GUI programs.
	b. We automatically generate 7 test cases using the file named "bigFile.txt"
	c. To run the test case generation, simply execute the python script named "sFileManipulation.py"
	d. The script doesn't require any input. It will manipulate the file using zip/unzip, encrypt/decrypt and split/merge combinations to generate 7 test cases.
	e. Each test case will manipulate a file named with test case number. For example, test case 5 will manipulate "bigFile5". This is easier for us the query the database and differentiate each test cases.
	f. All the generated files will be automatically removed once the test case is done.

II. Manual test case generation.
	a. This method is to generate test cases for normal activities.
	b. I generate test case by doing the following manually on a Windows machine:
		1. Copy the file named "bigFile.txt" to "bigFile - copy.txt"
		2. Rename the "bigFile - copy.txt' to "testfile.txt"
		3. Use Nodepad++ to modify the file "testfile.txt". Simply remove the first line.
		4. Use 7-zip to compress the file to "testfile.zip".
		5. Upload the file to Google Drive.
