# GDCDataRetrival
A script to retrieve data from NCI's GDC data protal

This script uses [gdctools](https://github.com/broadinstitute/gdctools) utilities created by Broad Institute.

It will download all files belonging to a particular data type in all Project IDs present in a Project.
All files will be downloaded in a /Data folder.

A folder will be created for each Project ID and inside that folder 10 files will be downloaded for each
work-flow type specified. The folder will also contain a summary of all the files downloaded in the form
of TSVs in a text file

The file structure looks something like this:
* Data  
 * TCGA-BRCA  
    * HTSeq - FPKM  
      * file1.txt.gz  
      * file2.txt.gz  
    * HTSeq - FPKM-UQ  
      * file1.txt.gz  
      * file2.txt.gz  
    * HTSeq - FPKM.txt  
    * HTSeq - FPKM-UQ  
 * TCGA-UCEC  
 * TCGA-KIRC  
 * TCGA-LUAD  
