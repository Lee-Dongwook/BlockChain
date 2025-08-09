export interface Contract {
  id: string;
  condition: string;
  action: string;
  expire_block?: number;
  executed: boolean;
}
