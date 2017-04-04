<?php

/** Change the namespace **/
namespace App\Helpers;
/** Change the namespace **/

use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\File\UploadedFile;

/*
 * This class is tightly-bound to Symfony's UploadedFile class and the Str facade
 * So it should only be used as a laravel component
 */

class StoreFile
{

    protected $file;
    protected $location;
    protected $full_filename;

    //Takes the file to be stored. It must be an instance of Symfony UploadedFile Class (used by Laravel)
    protected function setFile(UploadedFile $file) {
        $this->file = $file;
    }

    //Sets the location the file will be stored in
    protected function setFileLocation($location) {
        $this->location = $location;
    }

    //Generated a random name for the file and appends its extension (Ashe's convention for storing a file)
    //You must specify the length of the file name as an argument (int)
    protected function generateRandomName($length) {
        $this->full_filename = Str::random($length) . '.' . $this->file->getClientOriginalExtension();
    }

    //A method that wraps the UploadedFile move method and optimizes it for this class
    protected function mover() {
        $this->file->move($this->location, $this->full_filename);
    }

    //Finally, the one public method that does everything for you and also returns the full file path for you
    // to store in the database
    /**
     * @param UploadedFile $file
     * @param $location
     * @param $length
     * @return string
     */
    public function move(UploadedFile $file, $location, $length = 16) {
        $this->setFile($file);
        $this->setFileLocation($location);
        $this->generateRandomName($length);
        $this->mover();
        return $this->full_filename;
    }


}