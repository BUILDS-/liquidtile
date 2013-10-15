# liquidserial: The Serial Protocol Behind liquidtile

The problem: we need a serial protocol. One which is fast for our needs and natural to the
way we will be doing processing. 

## liquidserial v1 (ASCII)

The first version of liquidserial is simple and is ASCII. Packets are formed as follows

| Start Packet | Pixel Address/Command           | Red                      | Green                    | Blue                     | End Packet  |
|--------------|---------------------------------|--------------------------|--------------------------|--------------------------|-------------|
| ':'          | 0-15 (hex representation ascii) | 2 ascii characters (hex) | 2 ascii characters (hex) | 2 ascii characters (hex) | '\n'        |

For example, if I wanted to set pixel 5 to the color #ff0412 the following packet would be sent:

> :5ff0412\n

There is one special command implemented which is 'u' for update. If I wanted to send an update I would do the following.

> :u\n

## liquidserial v2 (Binary Data)

The liquidserial v1 protocol is not really well suited for frame updates, but it is very good for pixel based updates. It also limits us to a maximum
tile size of 4x4 without adding my ascii characters to the pixel address. Also for every byte of data we must send 2 characters, this is ok for small
tires, but will increase transmission time by a fair amount for larger tiles. A revision is needed.

The current proposed packet structure is:

| Name | Description                                      | Byte Length    | Notes |
|------|--------------------------------------------------|----------------|-------|
| SOP  | Starts the packet                                | 1              | 0xF1  |
| LEN  | Length of packet (not including LEN, SOP or EOP) | 2              |       |
| DATA | The datagram to be sent!                         | LEN bytes      |       |
| EOP  | End of packet                                    | 1              | 0xF2  |

There are two ways to end a packet:

1. Send LEN bytes in the data section followed by the EOP byte.
2. Wait for a transmission timeout to occur. This has yet to be specified, but will likely be around 10ms.

### Data format

| Byte Length        | Description |
|--------------------|-------------|
| 1                  | Command     |
| Defined by Command | Actual data being sent defined by what command is sent |

### Command Listing

- ACK (0x80)       - Acknwoledgement
- ERR (0x81)       - Error 
- PING (0x82)      - Ping
- WR_PIX (0x90)    - Write individual pixel values.
- WR_FRAME (0x91)  - Write a whole frame.
- WR_REG (0x92)    - Write control register.
- RD_PIX (0xa0)    - Read pixel
- RD_FRAME (0xa1)  - Read frame
- RD_REG (0xa2)    - Read control register status

#### ACK (0x80)

Most of the time no data is sent in ACK. However, ACK can also carry data for a 
read operation.

No Response

#### ERR (0x81)

Data is 1 byte long and contains an error code

| Error Code | Description       |
|------------|-------------------|
| 0x00       | General Error     | 
| 0x01       | Timeout Error     |
| 0x02       | Bad Packet Error  |
| 0x03       | Bad Address Error |

No Response

#### PING (0x82)

No data is sent in PING

Expected Response: ACK

#### WR_PIX (0x90)

Data format:

| Byte Length | Description |
|-------------|-------------|
| 2           | Address     |
| 1           | Red Color   |
| 1           | Green Color |
| 1           | Blue Color  |

Expected Response: ACK

#### WR_FRAME (0x91)

Sends color data for n pixels.

Data format:

| Byte Length | Description | 
|-------------|-------------|
| 1           | Red Pixel 0   
| 1           | Green Pixel 0 
| 1           | Blue Pixel 0  
| .           | .
| .           | .
| .           | .
| 1           | Red Pixel n-1 
| 1           | Green Pixel n-1
| 1           | Blue Pixel n-1

Expected Response: ACK

#### WR_REG (0x92) FIXME

Expected Response: ACK

#### ~RD_PIX (0xa0)~ FIXME

Expected Response: ACK with data
#### ~RD_FRAME (0xa1)~ FIXME

Expected Response: ACK with data

#### ~RD_REG (0xa2)~ FIXME

Expected Response: ACK with data
