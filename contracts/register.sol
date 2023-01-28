// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {

  address[] _usernames;
  uint[] _passwords;

  address[] _bidusernames;
  uint[] _bidpasswords;
  string[] _bidemails;

  mapping(address=>bool) users;
  mapping(address=>bool) bidders;

  function registeruser(address username,uint password) public{

    require(!users[username]);

    users[username]=true;
    _usernames.push(username);
    _passwords.push(password);
  }

  function viewusers() public view returns(address[] memory,uint[] memory){
    return(_usernames,_passwords);
  }

  function loginuser(address username,uint password) public view returns(bool){
    uint i=0;

    require(users[username]);

    for(i=0;i<_usernames.length;i++){
      if(username==_usernames[i] && password==_passwords[i]){
        return true;
      }
    }
    return false;
  }

  function registerbiduser(address username,uint password,string memory email) public{

    require(!bidders[username]);

    bidders[username]=true;
    _bidusernames.push(username);
    _bidpasswords.push(password);
    _bidemails.push(email);

  }
  
  function viewbidusers() public view returns(address[] memory ,uint[] memory,string[] memory){
    return(_bidusernames,_bidpasswords,_bidemails);
  }

  function loginbiduser(address username,uint password) public view returns(bool){
    uint i=0;

    require(bidders[username]);
    for(i=0;i<_bidusernames.length;i++){
      if(username==_bidusernames[i] && password==_bidpasswords[i]){
        return true;
      }
    }
    return false;
  }
}
