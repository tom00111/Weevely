//Author:  Carlo Satta
//Arguments: url of file, path on server 
//Description: Download a file.
echo "Downloaded".file_put_contents($ar[1], file_get_contents($ar[0]))." byte.\n";

