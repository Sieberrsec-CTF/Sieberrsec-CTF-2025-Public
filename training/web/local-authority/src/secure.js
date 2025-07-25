


function checkPassword(username, password)
{    
  console.log(username);
  console.log(password);
  if( username === 'admin' && password === 'strongPassword098765' )
  {
    return true;
  }
  else
  {
    return false;
  }
}

