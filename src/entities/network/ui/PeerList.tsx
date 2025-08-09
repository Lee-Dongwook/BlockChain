import React from "react";
import { Peer } from "../model";

interface Props {
  peers: Peer[];
}

export const PeerList: React.FC<Props> = ({ peers }) => {
  return (
    <div>
      <h3>Connected Peers</h3>
      <ul>
        {peers.map((peer) => (
          <li key={peer.id}>
            {peer.address} {peer.latency ? `(${peer.latency}ms)` : ""}
          </li>
        ))}
      </ul>
    </div>
  );
};
