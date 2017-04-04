<?php
/**
 * Created by PhpStorm.
 * User: omar
 * Date: 07/12/15
 * Time: 02:21 ص
 */

namespace App\VerificationBox\EmailSender;


use App\SuperModel\SuperModel;

interface EmailSenderInterface
{
    public function insertTempRecord(SuperModel $old_model, $new_record, $confirmation_column);
}