<?php
/**
 * Created by PhpStorm.
 * User: omar
 * Date: 07/12/15
 * Time: 02:24 ص
 */


namespace App\VerificationBox\EmailSender;

use \App\SuperModel\SuperModel;
use Illuminate\Support\Facades\Mail;
use \App\VerificationBox\MailConfig;
class EmailSender
{
    protected $last_record;

    protected $email_from;
    protected $name_from;
    protected $email_to;
    protected $name_to;
    protected $subject;

    protected $views;
    protected $confirmation_params;

    public function __construct()
    {
        $this->config = new MailConfig();
        $this->email_from               =   $this->config->email_from;
        $this->name_from                =   $this->config->name_from;
        $this->subject                  =   $this->config->subject;
        $this->views                    =   $this->config->views;
        $this->confirmation_column      =   $this->config->confirmation_column;
        $this->confirmation_code_length =   $this->config->confirmation_code_length;
        $this->confirmation_parameters  =   $this->config->confirmation_parameters;
        $this->confirmation_url         =   $this->config->confirmation_url;

    }

    protected function randStrGen($code_length){
        $result = "";
        $chars = "abcdefghijklmnopqrstuvwxyz0123456789";
        $charArray = str_split($chars);
        for($i = 0; $i < $code_length; $i++){
            $randItem = array_rand($charArray);
            $result .= "".$charArray[$randItem];
        }
        return $result;
    }



    protected function insertTempRecord(SuperModel $old_model, $new_record, $confirmation_column, $code_length)
    {
        // TODO: Implement insertTempRecord() method.
        $code = md5($this->randStrGen($code_length));
        $new_record[$confirmation_column] = $code;
        $this->last_record = $old_model->createByParams($new_record);
    }

    protected function mailer($confirmation_url, $email_to, $name_to) {
        $this->confirmation_params['confirmation_url'] = $confirmation_url;
        $this->email_to = $email_to;
        $this->name_to = $name_to;
        Mail::send($this->views, $this->confirmation_params, function ($message) {
            $message->subject($this->subject);
            $message->from($this->email_from, $this->name_from);
            $message->to($this->email_to, $this->name_to);
        });
        if(count(Mail::failures()) > 0) {
            return false;

        }
        return true;
    }



    protected function setConfirmationParams($params) {
        $confirmation_params = [];
        foreach ($params as $param) {
            $confirmation_params[$param] = $this->last_record[$param];
        }
        $this->confirmation_params = $confirmation_params;
    }

    /**This does the following:
     *  -inserts the temporary record into the temporary model
     *  -sets the confirmation parameters. These will be available to the view containing the confirmation link.
     *
     *
     * @param SuperModel $old_model
     * @param $new_record
     * @param $email_to
     * @param $name_to
     * @return bool
     */
    public function sendMail(SuperModel $old_model, $new_record, $email_to, $name_to) {
        $this->insertTempRecord($old_model, $new_record, $this->confirmation_column, $this->confirmation_code_length);
        $this->setConfirmationParams($this->confirmation_parameters);
        return $this->mailer($this->confirmation_url, $email_to, $name_to);
    }

    public function confirmedMail(SuperModel $new_model, $mail) {
        if (count($new_model->where( [$mail[0] => $mail[1]] )->first()) > 0) {
            return False;
        }
        return True;
    }


}