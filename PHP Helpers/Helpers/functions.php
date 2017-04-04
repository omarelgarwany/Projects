<?php
use Tymon\JWTAuth\Facades\JWTAuth;
use Illuminate\Http\Request;
use App\Exceptions\UserNotFoundException;
use App\Exceptions\InvalidCredentialsException;
use App\Exceptions\UserNotAuthorizedException;
use Illuminate\Support\Facades\Auth;

function dropdown_generator($arr_obj, array $key_val, array $prepend = [], array $append = []) {
    $new_arr = $prepend;
    foreach($arr_obj as $item) {
        foreach ($key_val as $key => $val) {
            $new_arr[$item[$key]] = $item[$val];

        }
    }
    foreach ($append as $append_key => $append_val) {
        $new_arr[$append_key] = $append_val;

    }
    return $new_arr;

}

function random_alphanumeric($length) {
    $characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
    $string = '';
    for ($i = 0; $i < $length; $i++) {
        $string .= $characters[rand(0, strlen($characters) - 1)];
    }
    return $string;
}

function loginUser(array $credentials) {

    if (! $token = JWTAuth::attempt($credentials)) {
        throw new InvalidCredentialsException;
    }
    $user = JWTAuth::setToken($token)->authenticate();
    return ['success' => true, 'token' => $token, 'user_id' => (string) $user->id];

}
function loginUserWithoutPassword(array $identifiers) {
    $user = (new \App\User)->where($identifiers)->first();
    if (! $token = JWTAuth::fromUser($user)) {
        throw new InvalidCredentialsException;
    }
    $user = JWTAuth::setToken($token)->authenticate();
    return ['success' => true, 'token' => $token, 'user_id' => (string) $user->id];

}
function authenticateToken() {
    if (! $user = JWTAuth::parseToken()->authenticate()) {
        throw new UserNotFoundException;
    }
    return $user;
}

function loginAdmin(array $credentials) {
    if (Auth::attempt($credentials)) {
        $user = Auth::user();
        if ($user->admin) {
            return $user;
        }
    }
    return null;
}

function getAttributesIfExist(Request $request, array $attributes) {
    $request_params = [];
    foreach ($attributes as $attribute) {
        if ($request->exists($attribute)) {
            $request_params[$attribute] = $request->get($attribute);
        } else {
            $request_params[$attribute] = null;

        }
    }
    return $request_params;
}

function frand($min, $max, $decimals = 0) {
    $scale = pow(10, $decimals);
    return mt_rand($min * $scale, $max * $scale) / $scale;
}


function sendNotification($gcm_ids, $message, $device){
    $app_key = 'AIzaSyCMenJdQb7FEo8qsD0b1Y-JE1YSKPh6bdI';
    $data = array(
        "registration_ids" => $gcm_ids,
        "data" => array(
            "message" => $message
        ),
        "priority" => "high",

    );
    if($device == 'ios')
    {
        $data['notification'] =
        [
            "sound" => "default",
            "title" => "Notification",
            "icon" => "@drawable/ic_launcher",
            "body" => $message
        ];
    }
    $data_string = json_encode($data);

    $ch = curl_init('https://gcm-http.googleapis.com/gcm/send');
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Authorization: key=' . $app_key,
        'Content-Type: application/json',
        'Content-Length: ' . strlen($data_string))
    ); 

    $result = curl_exec($ch);
    return $result;
}