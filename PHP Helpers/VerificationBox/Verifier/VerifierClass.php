<?php
/**
 * Created by PhpStorm.
 * User: omar
 * Date: 04/12/15
 * Time: 02:52 م
 */

namespace App\VerificationBox\Verifier;
use \App\VerificationBox\CarrierUtils\CarrierClass;
use \App\SuperModel\SuperModel;

class VerifierClass extends CarrierClass implements VerifierInterface
{

    public function setIdentifiers($identifiers) {
        $this->setLabels($identifiers);
    }
    public function verify(SuperModel $old_model, SuperModel $new_model)
    {
        $this->grabRow($old_model);
        $this->putRow($new_model);
    }

}