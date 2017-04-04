<?php
/**
 * Created by PhpStorm.
 * User: omar
 * Date: 07/12/15
 * Time: 01:54 م
 */
namespace App\VerificationBox;



class MailConfig {
    public function __construct()
    {
    $this->email_from                   =  'noreply@donation.com';
    $this->name_from                    =  'Resala';
    $this->subject                      =  'Confirm Donation';
    $this->views                        =  ['mails.confirm', 'mails.plain'];
    $this->confirmation_column          =  'confirm_code';
    $this->confirmation_code_length     =  10;
    $this->confirmation_parameters      =  ['id', 'confirm_code'];
    $this->confirmation_url             =  'http://46.101.115.109/resala-production/public/donor/confirm';


    }
}








