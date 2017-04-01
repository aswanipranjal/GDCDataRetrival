# GDCDataRetrival
A script to retrieve data from [NCI's GDC data portal](https://portal.gdc.cancer.gov/) to be used by the Xena browser created by [UCSC Xena](http://xena.ucsc.edu/)

Both the scripts use [gdctools](https://github.com/broadinstitute/gdctools) utilities created by Broad Institute.
(I did teeny tiny modifications and created some functions)

It will download all files belonging to a particular data type in all Project IDs present in a Project.
All files will be downloaded in a folder. 

```
sample_one.py 
This file labels the columns according to the file name.
```
```
sample_two.py 
This file labels the columns according to the submitter id, ex: TCGA-AB-C123
```

A folder will be created for each Project ID and inside that folder 10 files will be downloaded for each
work-flow type specified. The folder will also contain a summary of all the files downloaded in the form
of TSVs in a text file.

The file structure looks something like this:
```
* Data  
   * TCGA-BRCA  
      * HTSeq - FPKM  
         * file1.txt.gz  
         * file2.txt.gz  
      * HTSeq - FPKM-UQ  
         * file1.txt.gz  
         * file2.txt.gz  
      * HTSeq - FPKM.txt  
      * HTSeq - FPKM-UQ.txt  
   * TCGA-UCEC  
   * TCGA-KIRC  
   * TCGA-LUAD  
```

you can download the necessary modules using pip
```
pip install -r requirements.txt
```
