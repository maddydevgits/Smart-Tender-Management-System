// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract tender {

  address[] _tenderowners;
  uint[] _tenderids;
  string[] _tenderinfos;
  bool[] _tenderstates;
  address[] _tenderbidders;

  address[] _bidders;
  uint[] _bidtenderids;
  string[] _bidemails;
  uint[] _bidamounts;

  mapping(uint=>bool) tid;
  mapping(address=>bool) bidders;
  mapping(uint=>bool) tenderfinalids;

  function createtender(address tenderowner,uint tenderid,string memory tenderinfo) public{
    require(!tid[tenderid]);

    tid[tenderid]=true;
    _tenderowners.push(tenderowner);
    _tenderids.push(tenderid);
    _tenderinfos.push(tenderinfo);
    _tenderstates.push(true);
    _tenderbidders.push(tenderowner);
  }

  function viewtenders() public view returns(address[] memory,uint[] memory,string[] memory,bool[] memory,address[] memory){
    return(_tenderowners,_tenderids,_tenderinfos,_tenderstates,_tenderbidders);
  }

  function gettender(uint tenderid) public view returns(address ,uint,string memory,bool,address){
    require(tid[tenderid]);
    uint i=0;
    for(i=0;i<_tenderids.length;i++){
      if(tenderid==_tenderids[i]){
        return(_tenderowners[i],_tenderids[i],_tenderinfos[i],_tenderstates[i],_tenderbidders[i]);
      }
    }
    return(msg.sender,0,"NA",false,msg.sender);
  }

  function bidtender(uint bidtenderid,uint bidamount,string memory bidemail) public{
    _bidtenderids.push(bidtenderid);
    _bidamounts.push(bidamount);
    _bidemails.push(bidemail);
    _bidders.push(msg.sender);
  }

  function viewbids() public view returns(uint[] memory,uint[] memory,string[] memory,address[] memory){
    return(_bidtenderids,_bidamounts,_bidemails,_bidders);
  }

  function allocatetender(uint tenderid,address bidowner) public{
    require(!tenderfinalids[tenderid]);
    uint i=0;

    tenderfinalids[tenderid]=true;
    for(i=0;i<_tenderids.length;i++){
      if(tenderid==_tenderids[i]){
        _tenderstates[i]=false;
        _tenderbidders[i]=bidowner;
      }
    }
  }
}
