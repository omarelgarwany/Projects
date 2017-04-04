<?php
/**
 * Created by PhpStorm.
 * User: omar
 * Date: 04/12/15
 * Time: 03:13 م
 */

namespace App\VerificationBox\Verifier;


use App\SuperModel\SuperModel;

interface VerifierInterface
{
    public function setIdentifiers($identifier);
    public function verify(SuperModel $old_model, SuperModel $new_model);
}