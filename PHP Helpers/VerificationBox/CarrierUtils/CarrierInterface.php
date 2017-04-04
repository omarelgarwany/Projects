<?php
/**
 * Created by PhpStorm.
 * User: omar
 * Date: 03/12/15
 * Time: 06:51 م
 */

namespace App\VerificationBox\CarrierUtils;

use App\SuperModel\SuperModel;

interface CarrierInterface
{
    public function grabRow(SuperModel $oldModel);
    public function putRow(SuperModel $newModel);
}